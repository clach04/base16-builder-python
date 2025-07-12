import os
import sys
import asyncio
import yaml
from collections import namedtuple
from contextlib import contextmanager

try:
    import colorama  # pip install colorama
except ImportError:
    colorama = None

is_win = sys.platform.startswith('win')
if is_win:
    use_color = False
else:
    use_color = True

if colorama:
    try:
        colorama.just_fix_windows_console()
    except AttributeError:
        # older version, for example '0.4.4'
        colorama.init()
    use_color = True

if os.environ.get('NO_COLOR') or not sys.stdout.isatty():  # NO_COLOR https://no-color.org/
    # skips processing for doing highlighting
    use_color = False


class JobOptions:
    """Container for options related to job processing"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


CWD = os.path.realpath(os.getcwd())
ACodes = namedtuple("ACodes", ["red", "yellow", "bold", "end"])
if use_color:
    acodes = ACodes(red="\033[31m", yellow="\033[33m", bold="\033[1m", end="\033[0m")
else:
    acodes = ACodes(red="", yellow="", bold="", end="")


@contextmanager
def compat_event_loop():
    """OS agnostic context manager for an event loop."""
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    event_loop = asyncio.get_event_loop()

    if event_loop.is_closed():
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

    yield event_loop

    event_loop.close()


def rel_to_cwd(*args):
    """Get absolute real path of $path with $CWD as base."""
    return os.path.join(CWD, *args)


def get_yaml_dict(yaml_file):
    """Return a yaml_dict from reading yaml_file. If yaml_file is empty or
    doesn't exist, return an empty dict instead."""
    try:
        with open(yaml_file, "r", encoding="utf-8") as file_:
            yaml_dict = yaml.safe_load(file_.read()) or {}
        return yaml_dict
    except FileNotFoundError:
        return {}


def err_print(msg, exit_code=1):
    """Print $msg and exit with $exit_code."""
    print(msg, file=sys.stderr)
    sys.exit(exit_code)


def verb_msg(msg, lvl=1):
    """Print a warning ($lvl=1) or an error ($lvl=2) message."""
    if lvl == 1:
        print(
            "{0.yellow}{0.bold}Warning{0.end}:\n{1}".format(acodes, msg),
            file=sys.stderr,
        )
    elif lvl == 2:
        print("{0.red}{0.bold}Error{0.end}:\n{1}".format(acodes, msg), file=sys.stderr)
