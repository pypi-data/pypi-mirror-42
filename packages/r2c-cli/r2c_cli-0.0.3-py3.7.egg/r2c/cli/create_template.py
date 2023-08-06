import json
import os
import shutil
import sys
from pathlib import Path

import click

DOCKER_FILE = """FROM ubuntu:17.10

RUN groupadd -r analysis && useradd --no-log-init --system --gid analysis analysis
USER analysis

COPY --chown=analysis:analysis src /analyzer
WORKDIR /
CMD ["/analyzer/analyze.sh"]"""

UNITTEST_SH = """#!/bin/bash

echo "⚠️ Empty unittest!"
"""

ANALYZE_SH = """#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/source-code"

echo "{\\"results\\": []}" | tee /analysis/output/output.json"""


def create_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, 0o775)


def create_template_analyzer(
    org: str,
    analyzer_name: str,
    author_name: str,
    author_email: str,
    run_on: str,
    output_type: str,
):
    analyzer_json_dict = {
        # TODO get from default org
        "analyzer_name": f"{org or 'example_org'}/{analyzer_name}",
        # "author_name": author_name,
        # "author_email": author_email,
        "version": "0.0.1",
        "spec_version": "1.0.0",
        "dependencies": {"public/source-code": "*"},
        "type": run_on,
        "output": output_type,
        "deterministic": True,
    }
    try:
        Path(os.path.join(analyzer_name, "src")).mkdir(parents=True)
        analyzer_json_path = os.path.join(analyzer_name, "analyzer.json")
        with open(analyzer_json_path, "w") as fp:
            json.dump(analyzer_json_dict, fp, indent=4)
        dockerfile_path = os.path.join(analyzer_name, "Dockerfile")
        with open(dockerfile_path, "w") as fp:
            fp.write(DOCKER_FILE)
        create_file(os.path.join(analyzer_name, "src", "analyze.sh"), ANALYZE_SH)
        create_file(os.path.join(analyzer_name, "src", "analyze.sh"), UNITTEST_SH)
    except FileExistsError as e:
        click.echo(f"❌ {analyzer_name} already exists. Please delete and run again")
        sys.exit(1)
    except Exception as e:
        click.echo(
            f"❌ There was an error. Please contact support at cli@ret2.co and ask for help: {e}"
        )
        sys.exit(1)
