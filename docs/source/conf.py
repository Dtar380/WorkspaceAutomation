# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'WorkSpace Automation'
copyright = '2024, Dtar380'
author = 'Dtar380'
version = '0.1.1'

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser"
]

templates_path = [
    '_templates'
]
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = [
    '_static'
]
