import argparse
import os
from pathlib import Path
from .resume import resume
from importlib import resources

# from importlib.resources.abc import Traversable
from pathlib import PosixPath
from typing import List
from shutil import copy2


def get_resources_nodes(root, tree, resrcs: List) -> List[PosixPath]:
    """_summary_
    Get resources nodes recursively.
    Parameters
    ----------
    root: root Traversable
        Directory containing the module
        Generally obtained with:
        `root=resources.files(package_name).parent`
        package_name, being the package installed on your system
    tree : Traversable
        _description_
    resrcs:
        Resources should be empty list for first call.
        Expands on each recursive call.

    Returns
    -------
    List[PosixPath]
        List of nodes which are resources

    Examples
    --------
    >>> a = resources.files("cliriculum.data")
    >>> get_resources_nodes(a.parent.parent, a)
    """
    package = ".".join(tree.relative_to(root).parts)  # init
    for node in tree.iterdir():
        # print(node)
        # print(package)
        # le node reste le node. Il faut l'updater
        if node.is_dir():
            # if (node / "__init__.py").exists():
            get_resources_nodes(root=root, tree=node, resrcs=resrcs)
        else:
            # node is file
            # print(node.name)
            # print(package)
            if (
                resources.is_resource(package, node.name)
                and node.parts[-1] != "__init__.py"
            ):
                resrcs.append(node)
    return resrcs


def copy_resources(directory: str, resource_root: str = "cliriculum.data"):
    """
    Copy resources to specified directory

    Parameters
    ----------
    directory: str Where to store the directory
    resource_root: str The resource_root directory specified in module type
    notation, default "cliriculum.data"
    """
    pkgname = resource_root.split(".")[0]

    tree = resources.files(package=resource_root)  # requires python >=3.9
    root = resources.files(package=pkgname).parent
    rsrcs = get_resources_nodes(root=root, tree=tree, resrcs=[])

    for source in rsrcs:
        relative_to = source.relative_to(tree)
        target_dir = Path(directory)
        target = target_dir / str(relative_to)
        
        # if source.relative_to is not root
        # and directory does not exist
        # create directory
        if target.parent.exists() is False and target.parent != target_dir:
            os.makedirs(target.parent)
        
        copy2(src=source, dst=target)


def make_resume(
    directory, sidebar_md: str, main_md: str, dates: str, contact: str, overwrite: bool
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
        sidebar_md=sidebar_md, main_md=sidebar_md, contact=contact, dates=dates
    )

    with open(Path(directory) / "index.html", "w") as f:
        f.write(html)

    # copy dependencies
    print(f"Copying files to {directory}")
    copy_resources(directory)


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a Resume using JSON and Markdown")
    parser.add_argument(
        "--main",
        dest="main_md",
        type=str,
        action="store",
        required=True,
        help="Path to the markdown file"
    )
    parser.add_argument(
        "--description",
        dest="descr_md",
        type=str,
        action="store",
        required=True
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
    return parser


def main():
    parser = cli()
    args = parser.parse_args()

    args.destination



if __name__ == "__main__":
    sys.exit(main())
