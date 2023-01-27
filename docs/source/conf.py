# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cliriculum'
copyright = '2022, Alexandre Sonderegger'
author = 'Alexandre Sonderegger'
from cliriculum import __version__
release = "v" + __version__
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'myst_parser', "sphinx.ext.autosummary", 'autoapi.extension']

html_theme = "furo"
autosummary_generate = True
autosummary_generate_overwrite = True

autoapi_dirs = ['../../cliriculum']
autoapi_add_toctree_entry = False
autoapi_ignore = ['*parsers.py']
autoapi_keep_files = False
