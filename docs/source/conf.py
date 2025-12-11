import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(root_dir)

from pypipedrive import __version__ as version

# Document Python Code
autoapi_type = "python"
autoapi_dirs = [os.path.join(root_dir, "pypipedrive")]

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = "pypipedrive"
copyright = "2025, Juan Manuel M. Pérez"
author = "Juan Manuel M. Pérez <jm@magicalpotion.io>"
release = version

__version__ = version.split("-")[0]
__release__ = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinxext.opengraph",
    "sphinx.ext.autosectionlabel",
    "sphinxcontrib.googleanalytics",
    "sphinxcontrib.autodoc_pydantic",
    "sphinxcontrib.jquery",
    "revitron_sphinx_theme",
]

# Options for sphinxcontrib-googleanalytics extension
googleanalytics_id = "G-8Q5M4DJNCK"

# Options for sphinxext-opengraph extension
ogp_site_url = "https://pypipedrive.readthedocs.io"
ogp_site_name = "CRM Pipedrive V1/V2 API Client for Python"
ogp_image = "https://pypipedrive.readthedocs.io/en/latest/_static/logo-text.svg"
ogp_description_length = 300
ogp_type = "article"
ogp_custom_meta_tags = [
    '<meta property="og:ignore_canonical" content="true" />',
]
ogp_enable_meta_description = True


templates_path = ["_templates"]
exclude_patterns = []

master_doc = "index"

html_title = ""
html_theme = "revitron_sphinx_theme"
html_static_path = ["_static"]

# Theme options are theme-specific and customize the look and feel of a theme
# further. For a list of options available for each theme, see the documentation.

html_theme_options = {
    # "color_scheme": "",
    # "canonical_url": "",
    # "analytics_id": "G-XXXXXXXXXX",
    # "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    # "navigation_depth": 4,
    # "includehidden": True,
    # "titles_only": False,
    "github_url": "https://github.com/jmanprz/pypipedrive",
    "logo_mobile": "logo-text.svg"
}

html_logo = "_static/logo.svg"

html_context = {
    "landing_page": {
        "menu": [
            {"title": "Pipedrive API Reference", "url": "https://developers.pipedrive.com/docs/api/v1"},
            # {"title": "♡ Sponsor", "url": "https://github.com/sponsors/jmanprz"},
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
# html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = []