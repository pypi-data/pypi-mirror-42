#!/usr/bin/env python3
import os
from distutils.util import strtobool

import click

from r2c.cli.core import cli

if __name__ == "__main__":
    try:
        cli(obj={}, prog_name="r2c")
    except Exception as e:
        debug = strtobool(os.getenv("DEBUG", "False"))
        if debug:
            click.echo(e)
        else:
            click.echo(
                f"❌ there was an unexpected error. Please use `r2c --debug <CMD>`, to get error log. For more help, reach out to R2C  at support@ret2.co"
            )
