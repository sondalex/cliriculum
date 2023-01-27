import argparse
import os
import sys
from pathlib import Path
from typing import Union
from cliriculum.resume import resume
from cliriculum.utils import copy_resources
from cliriculum.pdf import chromium_print


def make_resume(
    directory,
    sidebar_md: str,
    main_md: str,
    dates: str,
    contact: str,
    overwrite: bool,
    stylesheet: Union[str, None],
    location: Union[str, None] = None,
    output: Union[str, None] = None,
):
    """
    Generates resume

    See :py:mod:`cliriculum.resume`
    """
    if os.path.isdir(directory):
        os.makedirs(directory, exist_ok=overwrite)

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
    if output is not None:
        chromium_print(directory=directory, filename=output)


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
    parser.add_argument(
        "--pdf-output",
        dest="output",
        action="store",
        type=str,
        default=None,
        required=False,
        help="If filename the pdf will be generated and saved to '--directory + --pdf-output', if path like it will be saved to provided path",
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
        output=args.output,
    )


if __name__ == "__main__":
    sys.exit(main())
