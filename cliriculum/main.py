import argparse
import os
from pathlib import Path
from cliriculum.resume import resume
from cliriculum.utils import copy_resources
from typing import Union

# from importlib.resources.abc import Traversable


def make_resume(
    directory,
    sidebar_md: str,
    main_md: str,
    dates: str,
    contact: str,
    overwrite: bool,
    stylesheet: Union[str, None],
    location: Union[str, None] = None,
):
    """
    Generates resume

    See :py:mod:
    """
    if os.path.isdir(directory):
        if overwrite is True:
            pass
        else:
            error = """
            Folder already exists. If you wish to overwrite its content, set `overwrite` to True
            """
            raise FileExistsError(error)
    elif os.path.isfile(directory) is False:
        os.mkdir(directory)
    else:
        raise ValueError("The specified file is not a directory and exists")
    html = resume(
        sidebar_md=sidebar_md,
        main_md=main_md,
        contact=contact,
        dates=dates,
        rsrc_dst=directory,
        stylesheet=stylesheet,
        location=location,
    )

    with open(Path(directory) / "index.html", "w") as f:
        f.write(html)

    # copy dependencies
    print(f"Copying files to {directory}")
    copy_resources(directory)


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a Resume using JSON and Markdown"
    )
    parser.add_argument(
        "--main",
        dest="main_md",
        type=str,
        action="store",
        required=True,
        help="Path to the markdown file",
    )
    parser.add_argument(
        "--description", dest="descr_md", type=str, action="store", required=True
    )
    parser.add_argument(
        "--dates",
        dest="dates_json",
        type=str,
        action="store",
        required=True,
        help="Path to the dates JSON file",
    )
    parser.add_argument(
        "--contact",
        dest="contact_json",
        type=str,
        action="store",
        required=True,
        help="Path to the contact JSON file",
    )

    parser.add_argument(
        "--destination",
        dest="destination",
        type=str,
        action="store",
        required=False,
        help="Directory where the HTML resume should be created",
        default="resume",
    )

    parser.add_argument(
        "--overwrite",
        type=int,
        action="store",
        required=False,
        help="Overwrite existing directory if set to other value than 0.",
        default=0,
    )
    parser.add_argument(
        "--stylesheet",
        dest="stylesheet",
        type=str,
        action="store",
        required=False,
        help="A supplementary stylesheet to add to the dom.",
        default=None,
    )
    parser.add_argument(
        "--location",
        dest="location",
        type=str,
        action="store",
        required=False,
        help="A file specifying locations to map to 2nd level headers by id",
        default=None,
    )
    return parser


def main():
    parser = cli()
    args = parser.parse_args()
    overwrite = bool(args.overwrite)
    make_resume(
        directory=args.destination,
        sidebar_md=args.descr_md,
        contact=args.contact_json,
        dates=args.dates_json,
        main_md=args.main_md,
        overwrite=overwrite,
        stylesheet=args.stylesheet,
        location=args.location,
    )


if __name__ == "__main__":
    sys.exit(main())
