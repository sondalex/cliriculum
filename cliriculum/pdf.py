"""
Utilities to render the generated resume from html to pdf.
"""

import os
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from shutil import which
from threading import Thread
from typing import Union

EXTRA_ARGS = [
    "--run-all-compositor-stages-before-draw",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--hide-scrollbars",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-software-rasterizer",
]


def check_dependency(entrypoints):
    """
    Check if a dependency command line is available.


    Parameters
    ----------
    entrypoints: List[str]
        A list of synonym command line entry points.

    """
    value = False
    for entrypoint in entrypoints:
        cmd = which(entrypoint)
        if cmd is not None:
            value = entrypoint
            break
    return value


class DependencyError(Exception):
    pass


# Rather than relying on metaclass, which would allow setting the directory parameter dynamically by creating multiple classes as in
# https://stackoverflow.com/questions/39801718/how-to-run-a-http-server-which-serves-a-specific-path
# I chose just setting a context manager which changes the current directory.
# This choice might change to metaclass, if more evidence of benefits of this method appears in the future
# Current choice, avoids setting directory which is an argument added in Python 3.7 only


class ChDir:
    """
    Context manager to temporarily change directory.

    Example
    -------
    Use with http server
    Imagine an index.html is in the resume folder.
    >>> from http.server import HTTPServer, SimpleHTTPRequestHandler
    >>> from cliriculum.pdf import ChDir
    >>> with ChDir("resume/"):
    >>>     httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    >>>     httpd.serve_forever()
    """

    def __init__(self, target: Union[str, os.PathLike]):
        # current dir
        # Checks
        if isinstance(target, (os.PathLike, str)) is False:  # check type
            raise TypeError("Only os.PathLike or str types are accepted.")
        # Convert to str absolute path

        target = os.path.abspath(target)  # pathlike automatically converted to str
        self.origin = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self.origin)


def chromium_print(
    directory: Union[str, os.PathLike],
    filename: str = "output.pdf",
    port: int = 8000,
    timeout: int = 3000,
    verbose: bool = False,
    headless: bool = True,
):
    """

    Parameters
    ----------
    directory : Union[str, os.PathLike]
        Directory of the HTML resume
    filename : str, optional
        Name of the converted document, by default "output.pdf"
        Passed to headless chromium.
        **Note**: Can also be a a path (abs or relative).
    port : int, optional
        The network port , by default 8000
        If you wish automatic port selection set this value to 0.
    timeout: int
        Time to wait.
        See `chromium new-headless <https://developer.chrome.com/docs/chromium/new-headless#--timeout>`_
        by default 3000 (3 seconds)
    headless: bool
        Defaults to True

    Raises
    ------
    DependencyError
    subprocess.SubprocessError
    """
    cli_deps = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]
    ch_deps = check_dependency(cli_deps)
    if ch_deps is False:
        raise DependencyError
    with ChDir(directory):
        httpd = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
        thread_server = Thread(target=httpd.serve_forever)
        thread_server.start()
        named_args = [f"--timeout={timeout}", f"--print-to-pdf={filename}"]
        arg = []
        if headless is True:
            arg = ["--headless='new'"]
        cmd = [ch_deps] + arg + named_args + EXTRA_ARGS + [f"http://127.0.0.1:{port}"]
        if verbose is True:
            print(" ".join(cmd))
        process = subprocess.run(
            cmd,
            timeout=30,
        )
        if process.returncode != 0:
            raise subprocess.SubprocessError(f"return code: {process.returncode}")
        httpd.shutdown()
