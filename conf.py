# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'openheating'
copyright = '2020, Jörg Faschingbauer'
author = 'Jörg Faschingbauer'

# The full version, including alpha/beta/rc tags
release = '0.0.0'


# -- General configuration ---------------------------------------------------
master_doc = 'README'  # github won't render index.rst, so we name it
                       # README.rst

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
]
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# THEMES. tried a few, looking out for good
# navigation/location-feedback. the most customizable (so far) is the
# "Read The Docs" theme.

# ---
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': -1,
}

# ---
# html_theme = 'alabaster'
# html_theme_options = {
#     'fixed_sidebar': True,
# }

# ---
# # https://github.com/ryan-roemer/sphinx-bootstrap-theme
# import sphinx_bootstrap_theme
# html_theme = 'bootstrap'
# html_theme_options = {
# }
# html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# ---
# import cloud_sptheme
# html_theme = 'cloud'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

# html_static_path = ['_static']
