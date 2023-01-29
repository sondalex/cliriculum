from typing import Union, List, Iterable
from pathlib import PosixPath, Path
from shutil import copy2
from importlib import resources
import os


def get_resources_nodes(root, tree, resrcs: List, skip_dirs: Iterable = {"__pycache__"}) -> List[PosixPath]:
    """
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
    skip_dirs: Iterable
        Directories in which resources should not be fetched.
        Default = {'__pycache__'}
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
        if node.is_dir() and node.parts[-1] not in set(skip_dirs):
            get_resources_nodes(root=root, tree=node, resrcs=resrcs)
        else:
            print(f"package: {package}, node: {node}")
            if (
                resources.files(package).joinpath(node).is_file()
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
        # assert False == True


def copy_files(srcs: Iterable[Union[str, Path]], dst: Union[Path, str]) -> None:
    """
    Copy files to destination keeping path basename.

    Parameters
    ----------
    srcs : Iterable[Union[str, Path]]
        _description_
    dst : Union[Path, str]
        _description_
    """
    # effectivement peut etre très dangereux.
    # Doit etre corriger.
    if isinstance(srcs, str):
        raise TypeError("srcs should be an Iterable but not a string")
    for src in srcs:
        file_dst = Path(dst) / os.path.basename(src)
        copy2(src, file_dst)
