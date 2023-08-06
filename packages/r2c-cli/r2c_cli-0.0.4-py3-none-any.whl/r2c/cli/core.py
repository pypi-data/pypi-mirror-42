#!/usr/bin/env python3
import json
import logging
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

import click
import requests

from r2c.cli.create_template import create_template_analyzer
from r2c.lib.manifest import AnalyzerManifest
from r2c.lib.registry import RegistryData
from r2c.lib.run import (
    build_docker,
    docker_image,
    integration_test,
    run_analyzer_on_local_code,
    run_docker_unittest,
)
from r2c.lib.util import analyzer_name_from_dir
from r2c.lib.versioned_analyzer import AnalyzerName

logger = logging.getLogger(__name__)
LOCAL_CONFIG_DIR = os.path.join(Path.home(), ".r2c")
CONFIG_FILENAME = "config.json"
CREDS_FILENAME = "credentials.json"
LOCAL_DEV = os.getenv("LOCAL_DEV") == "True"
MAX_RETRIES = 3


def fetch_registry_data():
    org = get_default_org()
    try:
        url = f"{get_base_url()}/api/v1/analyzers/"
        r = auth_get(url)
        r.raise_for_status()

        response_json = r.json()
        if response_json["status"] == "success":
            return response_json["analyzers"]
        else:
            raise ValueError("Couldn't parse analyzer registry response")
    except Exception as e:
        logger.exception(e)
        click.echo("❌ unable to obtain data about dependencies. Contact R2C support")
        raise


def open_browser_login(org):
    url = f"{get_base_url(org)}/settings/token"
    click.echo(f"trying to open {url} in your browser...")
    webbrowser.open(url, new=0, autoraise=True)


def validate_token(org, token):
    try:
        r = auth_get(f"{get_base_url(org)}/settings", token=token)
        return r.status_code == requests.codes.ok
    except Exception as e:
        # TODO log exception
        return False


def abort_on_build_failure(build_status):
    if build_status != 0:
        logger.error(f"failed to build docker image: {build_status}")
        sys.exit(build_status)


def save_json(obj, filepath):
    with open(filepath, "w") as fp:
        json.dump(obj, fp, indent=4, sort_keys=True)


def load_creds():
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    try:
        with open(cred_file) as fp:
            return json.load(fp)
    except Exception as e:
        logger.info(f"unable to read token file from {cred_file}: {e}")
        return {}


def save_config_creds(org, token):
    Path(LOCAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    config_file = os.path.join(LOCAL_CONFIG_DIR, CONFIG_FILENAME)
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    save_json({"defaultOrg": org}, config_file)
    creds = load_creds()
    new_creds = {**creds, org: token}
    save_json(new_creds, cred_file)


def delete_all_creds():
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    save_json({}, cred_file)


def delete_creds(org):
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    creds = load_creds()
    if org in creds:
        del creds[org]
    save_json(creds, cred_file)


def get_token_for_org(org):
    Path(LOCAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    cred_file = os.path.join(LOCAL_CONFIG_DIR, CREDS_FILENAME)
    if os.path.exists(cred_file):
        try:
            with open(cred_file) as fp:
                cred_map = json.load(fp)
                return cred_map.get(org)
        except Exception as e:
            logger.info(
                f"unable to load token for {org} from the {cred_file} credentials file",
                e,
            )  # TODO use logger
            return None
    else:
        return None


def get_default_org():
    Path(LOCAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    config_file = os.path.join(LOCAL_CONFIG_DIR, CONFIG_FILENAME)
    if os.path.exists(config_file):
        try:
            with open(config_file) as fp:
                config = json.load(fp)
                return config.get("defaultOrg")
        except Exception as e:
            logger.info(
                f"unable to load defaultOrg from the {config_file} config file", e
            )  # TODO use logger
    return None


def get_default_token():
    org = get_default_org()
    if org:
        return get_token_for_org(org)
    else:
        return None


def get_base_url(org=get_default_org(), local_dev=LOCAL_DEV):
    if local_dev:
        return "http://localhost:5000"
    elif org:
        return f"https://{org}.massive.ret2.co"
    else:
        logger.info("No org set so going to use 'public' org")
        return f"https://public.massive.ret2.co"


def get_auth_header(token):
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        return {}


def auth_get(url, params={}, headers={}, token=get_default_token()):
    headers = {"Accept": "application/json", **headers, **get_auth_header(token)}
    r = requests.get(url, headers=headers, params=params)
    return r


def auth_post(url, data={}, params={}, headers={}, files={}, token=get_default_token()):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **headers,
        **get_auth_header(token),
    }
    r = requests.post(url, headers=headers, params=params, data=data, files={})
    return r


def auth_put(url, data={}, params={}, headers={}, files={}, token=get_default_token()):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **headers,
        **get_auth_header(token),
    }
    r = requests.put(url, headers=headers, params=params, data=data, files={})
    return r


def auth_delete(
    url, data={}, params={}, headers={}, files={}, token=get_default_token()
):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        **headers,
        **get_auth_header(token),
    }
    r = requests.delete(url, headers=headers, params=params, data=data, files={})
    return r


def upload_analyzer_json(analyzer_directory):
    path = os.path.join(analyzer_directory, "analyzer.json")
    logger.info(f"Uploading analyzer.json from {path}")
    with open(path) as fp:
        analyzer_json = json.load(fp)
    r = auth_post(f"{get_base_url()}/api/v1/analyzers/", data=json.dumps(analyzer_json))
    r.raise_for_status()
    data = r.json()
    link = data.get("links", {}).get("artifact_url")
    return link


def get_docker_creds(artifact_link):
    if LOCAL_DEV:
        return {}
    r = auth_get(artifact_link)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data.get("credentials")
    else:
        return None


def docker_login(creds):
    docker_login_cmd = [
        "docker",
        "login",
        "-u",
        creds.get("login"),
        "-p",
        creds.get("password"),
        creds.get("endpoint"),
    ]
    if LOCAL_DEV:
        logger.info(f"Using ecr credentials in .aws during development")
        try:
            erc_login = subprocess.check_output(
                [
                    "aws",
                    "ecr",
                    "get-login",
                    "--no-include-email",
                    "--region",
                    "us-west-2",
                ]
            )
            docker_login_cmd = erc_login.decode("utf-8").strip().split(" ")
        except Exception as e:
            logger.info(f"Docker login failed with {e}")
            return True
    logger.info(f"Running login with {' '.join(docker_login_cmd)}")
    return_code = subprocess.call(docker_login_cmd)
    return return_code == 0


def docker_push(docker_image_tag):
    docker_push_cmd = ["docker", "push", docker_image_tag]
    logger.info(f"Running push with {' '.join(docker_push_cmd)}")
    return_code = subprocess.call(docker_push_cmd)
    return return_code == 0


def get_git_author():
    try:
        git_name = (
            subprocess.check_output(["git", "config", "--get", "user.name"])
            .decode("utf-8")
            .strip()
        )
        git_email = (
            subprocess.check_output(["git", "config", "--get", "user.email"])
            .decode("utf-8")
            .strip()
        )
        return (git_name, git_email)
    except Exception as e:
        logger.info(e)
        return (None, None)


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    help="Show extra output, error messages, and exception stack traces",
    default=False,
)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    if debug:
        logging.basicConfig(level=logging.INFO)
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.option(
    "--org",
    help="org to sign into. Ask R2C if you have questions about this",
    required=False,
)
def login(org=None):
    """Log into the R2C analysis platform.

    Logging in will grant you access to private analyzers published to
    your org. After logging in, you can locally run analyzers that depend
    on these privately published analyzers.
    """

    # ensure org
    if org is None:
        org = get_default_org()
        if org is None:
            org = click.prompt("Please enter the org")
    # open sign in link
    open_browser_login(org)
    error = True
    # prompt for token
    for attempt in range(MAX_RETRIES):
        token = click.prompt("Please enter the API token")
        # validate token
        valid_token = validate_token(org, token)
        if valid_token:
            # save to ~/.r2c
            save_config_creds(org, token)
            click.echo("You are now logged in 🎉")
            error = False
            break
        else:
            click.echo("❌ invalid token. Please try again")
    if error:
        click.echo("💀 unable to validate the token. This is a fatal error 💀")
        sys.exit(1)


@cli.command()
@click.option(
    "--org",
    help="org to sign into. Ask R2C if you have questions about this",
    required=False,
)
def logout(org=None):
    """Log out of the R2C analysis platform.

    Logging out will remove all authentication tokens.
    If --org is specified, it will only remove the authentication token for that org
    """
    try:
        # ensure org
        if org is None:
            # remove all tokens
            delete_all_creds()
        else:
            # remove token for just that org
            delete_creds(org)
    except Exception as e:
        click.echo(
            f"❌ there was an unexpected error Please ask for help from R2C support@ret2.co"
        )
        logger.exception(e)
        sys.exit(1)


@cli.command()
@click.option("--analyzer_directory", default=os.getcwd())
@click.argument("env_args_string", nargs=-1, type=click.Path())
@click.pass_context
def unittest(ctx, analyzer_directory, env_args_string):
    """
    Locally unit tests for the current analyzer directory
    You can define how to run unittest in src/unittest.sh
    You may have to login if your analyzer depends on privately
    published analyzers."""
    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)

    analyzer_name = analyzer_name_from_dir(analyzer_directory)
    manifest_path = os.path.join(analyzer_directory, "analyzer.json")
    with open(manifest_path) as fp:
        version = json.load(fp)["version"]
    docker_image_link = docker_image(analyzer_name, version)

    abort_on_build_failure(
        build_docker(
            docker_image=docker_image_link,
            analyzer=".",
            version=version,
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    status = run_docker_unittest(
        analyzer_directory=analyzer_directory,
        analyzer_name=analyzer_name,
        docker_image=docker_image_link,
        verbose=debug,
        env_args_dict=env_args_dict,
    )
    if status == 0:
        logger.info(f"\n✅ unit tests passed")
        sys.exit(0)
    else:
        logger.error(f"\n❌ unit tests failed with status {status}")
        sys.exit(-1)


@cli.command()
@click.option("--analyzer_directory", default=".")
@click.argument("env_args_string", nargs=-1, type=click.Path())
@click.pass_context
def test(ctx, analyzer_directory, env_args_string):
    """
    Locally run integration tests for the current analyzer directory.
    You can add integration test files to the `examples/` directory.
    For more information, refer to the integration test section of the README.

    You may have to login if your analyzer depends on privately
    published analyzers."""

    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)
    click.echo(
        f"Running integration tests for analyzer with debug mode {'on' if ctx.obj['DEBUG'] else 'off'}"
    )

    analyzer_name = analyzer_name_from_dir(analyzer_directory)
    manifest_path = os.path.join(analyzer_directory, "analyzer.json")
    with open(manifest_path) as fp:
        version = json.load(fp)["version"]

    abort_on_build_failure(
        build_docker(
            docker_image=docker_image(analyzer_name, version),
            analyzer=".",
            version=version,
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    integration_test(
        analyzer_directory,
        workdir=None,
        env_args_dict=env_args_dict,
        registry_data=RegistryData.from_json(fetch_registry_data()),
    )


@cli.command()
@click.option("--analyzer_directory", default=os.getcwd())
@click.argument("env_args_string", nargs=-1, type=click.Path())
@click.pass_context
def push(ctx, analyzer_directory, env_args_string):
    """Push the analyzer in the current directory to the R2C analysis platform.

    You must login required to push analyzers.

    This command will validate your analyzer and privately publish your analyzer
    to your org with the name specified in analyzer.json.

    Your analyzer name must follow {org}/{name}."""
    debug = ctx.obj["DEBUG"]
    env_args_dict = parse_remaining(env_args_string)

    analyzer_name = analyzer_name_from_dir(analyzer_directory)
    manifest_path = os.path.join(analyzer_directory, "analyzer.json")

    with open(manifest_path, encoding="utf-8") as f:
        analyzer_json = json.load(f)
        version = analyzer_json.get("version")
    click.echo(f"Pushing analyzer in {analyzer_directory}...")
    # upload analyzer.json
    artifact_link = upload_analyzer_json(analyzer_directory)
    if artifact_link is None:
        click.echo(
            "❌ there was an error uploading analyzer. Please ask for help from R2C support"
        )
        sys.exit(1)
    # get docker login creds
    creds = get_docker_creds(artifact_link)
    if creds is None:
        click.echo(
            "❌ there was an error getting docker credentials. Please ask for help from R2C support"
        )
        sys.exit(1)
    # docker login
    successful_login = docker_login(creds)
    if not successful_login:
        click.echo(
            "❌ there was an error logging into docker. Please ask for help from R2C support"
        )
        sys.exit(1)
    # docker build and tag
    image_tag = docker_image(analyzer_name, version)
    abort_on_build_failure(
        build_docker(
            docker_image=image_tag,
            analyzer=".",
            version=version,
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    # docker push
    successful_push = docker_push(image_tag)
    if not successful_push:
        click.echo(
            "❌ there was an error pushing the docker image. Please ask for help from R2C support"
        )
        sys.exit(1)
    # mark uploaded with API
    # TODO figure out how to determine org from analyzer.json
    uploaded_url = (
        f"{get_base_url()}/api/v1/analyzers/{analyzer_name}/{version}/uploaded"
    )
    r = auth_put(uploaded_url)
    r.raise_for_status()
    data = r.json()
    if data.get("status") == "uploaded":
        web_url = data.get("links").get("web_url")
        # display status to user and give link to view in web UI
        click.echo(f"✅ successfully uploaded analyzer. Web url for analyzer {web_url}")
    else:
        click.echo(
            "❌ there was an error marking the image as uploaded. Please ask for help from R2C support"
        )
        sys.exit(1)


def parse_remaining(pairs):
    """
    Given a string of remaining arguments (after the "--"), that looks like "['x=y', 'a=b'] return a dict of { 'x': 'y' }
    """
    return {pair.split("=")[0]: pair.split("=")[1] for pair in pairs}


@cli.command()
@click.option("--analyzer_directory", default=os.getcwd())
@click.option("--code", required=True)
@click.option(
    "--no_login",
    is_flag=True,
    default=False,
    help="Do not run `docker login` command during run.",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="don't start the container, wait for user",
)
@click.argument("env_args_string", nargs=-1, type=click.Path())
@click.pass_context
def run(ctx, analyzer_directory, code, no_login, wait, env_args_string):
    """Run the analyzer in the current directory over a code directory.

    You may have to login if your analyzer depends on privately
    published analyzers."""
    debug = ctx.obj["DEBUG"]
    click.echo(f"🏃 Running analyzer...{'with debug mode' if debug else ''}")
    env_args_dict = parse_remaining(env_args_string)

    analyzer_name = analyzer_name_from_dir(analyzer_directory)
    manifest_path = os.path.join(analyzer_directory, "analyzer.json")

    with open(manifest_path, encoding="utf-8") as f:
        manifest = AnalyzerManifest.from_json_str(f.read())

    dependencies = manifest.dependencies
    logger.info(f"{dependencies}")
    if len(dependencies) == 0:
        click.echo("❌ there was an error parsing dependencies")
        sys.exit(1)

    logger.info(f"Parsing and resolving dependencies")
    registry_data = RegistryData.from_json(fetch_registry_data())
    dep_name, dep_semver_version = next(iter(dependencies.items()))
    logger.info(f"Resolved version {dep_semver_version} for {dep_name}")
    dep_version = registry_data._resolve(AnalyzerName(dep_name), dep_semver_version)
    if not dep_version:
        click.echo(f"❌ there was an error resolving version {dep_semver_version}")
        sys.exit(1)

    if not no_login:
        artifact_link = (
            f"{get_base_url()}/api/v1/artifacts/{dep_name}/{dep_version.version}"
        )
        logger.info(f"Getting credential from {artifact_link}")

        # TODO use proper auth credential once its done
        creds = get_docker_creds(artifact_link)
        if creds is None:
            click.echo(
                "❌ there was an error getting docker credentials. Please ask for help from R2C support"
            )
            sys.exit(1)
        # docker login
        successful_login = docker_login(creds)
        if not successful_login:
            click.echo(
                "❌ there was an error logging into docker. Please ask for help from R2C support"
            )
            sys.exit(1)

    abort_on_build_failure(
        build_docker(
            docker_image=docker_image(analyzer_name, manifest.version),
            analyzer=".",
            version=manifest.version,
            env_args_dict=env_args_dict,
            verbose=debug,
        )
    )

    # idk why this is happening for quoted paths
    code_path = code.strip('"')

    run_analyzer_on_local_code(
        registry_data=registry_data,
        manifest=manifest,
        workdir=None,
        code_dir=code_path,
        wait=wait,
        no_preserve_workdir=True,
        report=False,
        env_args_dict=env_args_dict,
    )

    return


@cli.command()
@click.option("--analyzer_name")
@click.option("--author_name")
@click.option("--author_email")
@click.option("--run_on")
@click.option("--output_type")
@click.pass_context
def init(ctx, analyzer_name, author_name, author_email, run_on, output_type):
    """Creates an example analyzer for your choice of languages.

    Once you create your analyzer, you can navigate to the analyzer directory
    and run other `r2c` commands, like `run`, `test`, or `push`."""
    debug = ctx.obj["DEBUG"]
    default_name, default_email = get_git_author()
    if not analyzer_name:
        analyzer_name = click.prompt("Analyzer name", default="example")
    if not author_name:
        author_name = click.prompt("Author name", default=default_name)
    if not author_email:
        author_email = click.prompt("Author email", default=default_email)
    if not run_on:
        run_on = click.prompt(
            "Run on", default="commit", type=click.Choice(["constant", "commit", "git"])
        )
    if not output_type:
        output_type = click.prompt(
            "Output type",
            default="json",
            type=click.Choice(["filesystem", "json", "both"]),
        )
    create_template_analyzer(
        get_default_org(), analyzer_name, author_name, author_email, run_on, output_type
    )
    click.echo(f"✅ done. Your analyzer can be found in the {analyzer_name} directory")


if __name__ == "__main__":
    try:
        cli(obj={})
    except (KeyboardInterrupt, SystemExit):
        click.echo(f"exiting...")
        sys.exit(2)
    except Exception as e:
        click.echo(
            f"❌ there was an unexpected error Please ask for help from R2C support@ret2.co"
        )
        logger.exception(e)
