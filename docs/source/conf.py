import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

from pypipedrive import __version__ as version

# Document Python Code
autoapi_type = "python"
autoapi_dirs = [os.path.join(root_dir, "pypipedrive")]

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyPipedrive'
copyright = '2025, Gildas Tone'
author = 'Gildas Tone'
release = version

__version__ = version.split("-", 0)
__release__ = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# import revitron_sphinx_theme

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_title = ""
html_theme = "furo"
html_static_path = ['_static']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

# html_theme_options = {}
html_theme_options = {
    # "color_scheme": "",
    # "canonical_url": "",
    # "analytics_id": "UA-3836052-10",
    # "style_external_links": False,
    # "cols lapse_navigation": True,
    # "sticky_navigation": True,
    # "navigation_depth": 4,
    # "includehidden": True,
    # "titles_only": False,
    # "github_url": "https://github.com/gildastone/pypipedrive",
    # 'logo_mobile': 'demo/static/logo-mobile.svg'
    # "logo_mobile": "_static/logo.png",
}

# html_logo = 'demo/static/logo.svg'
html_logo = "_static/logo-text.svg"

html_context = {
    "landing_page": {
        "menu": [
            {"title": "Pipedrive Api Docs", "url": "https://developers.pipedrive.com/docs/api"},
            # {"title": "♡ Sponsor", "url": "https://github.com/sponsors/gtalarico"},
        ]
    },
    "docs_source_path": "docs/source",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
# html_css_files = ["custom.css"]
# html_js_files = []