import sys
import logging
import json
import click
import collections

from alfa_sdk.common.stores import ConfigStore
from alfa_cli.common.exceptions import AlfaCliError


class Logger:
    def __init__(self, *, verbose=None, pretty=None):
        if verbose is None:
            verbose = ConfigStore.get_value("verbose", False, is_boolean=True)

        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(format="%(message)s", level=log_level, stream=sys.stdout)

        self.verbose = verbose
        self.pretty = pretty

    def result(self, res):
        try:
            res = json.loads(str(res))
        except:
            pass

        if self.pretty:
            res = json.dumps(res, indent=4)
        else:
            res = json.dumps(res)

        click.echo(res)
        sys.exit(0)

    @classmethod
    def error(cls, err):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            message = "\n!!! {}".format(type(err).__name__)
            click.secho(message, err=True, fg="red")
            raise err

        # Parse Error Object

        message = str(err)
        error = None
        if hasattr(err, "kwargs") and "error" in err.kwargs:
            try:
                error = json.loads(err.kwargs.get("error"))

                if isinstance(error, collections.Mapping):
                    if "error" in error:
                        error = error.get("error")

                    if "stack" in error:
                        error.pop("stack")

                message = message.replace(err.kwargs.get("error"), "")
            except:
                pass

        # Print

        message = "!!! {}".format(message)
        click.secho(message, err=True, fg="red")
        if error is not None:
            error = json.dumps(error, indent=4)
            click.secho(error, err=True, fg="red")

        sys.exit(1)
