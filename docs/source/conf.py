import os
import sys

from ipykernel.kernelspec import install

from cliriculum import __version__


def setup_ipykernel(kernel_name: str):
    install(user=True, kernel_name=kernel_name)


setup_ipykernel("python3")

project = "cliriculum"
copyright = "2022, Alexandre Sonderegger"
author = "Alexandre Sonderegger"

release = "v" + __version__

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


html_theme = "alabaster"
html_static_path = ["_static"]


sys.path.insert(0, os.path.abspath("../.."))
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # 'myst_parser',
    "sphinx.ext.autosummary",
    "myst_nb",
    "sphinx.ext.autosectionlabel",
]

html_theme = "furo"
autosummary_generate = True
autosummary_generate_overwrite = True

autosectionlabel_prefix_document = True

nb_execution_mode = (
    "force"  # https://myst-nb.readthedocs.io/en/latest/configuration.html
)
# https://myst-nb.readthedocs.io/en/latest/computation/execute.html
autoclass_content = "both"
