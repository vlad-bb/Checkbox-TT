# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('..'))

# Mock external dependencies for documentation building
import unittest.mock

MOCK_MODULES = [
    'uvicorn',
    'fastapi',
    'fastapi.security',
    'fastapi.templating',
    'fastapi.staticfiles',
    'fastapi.middleware.cors',
    'sqlalchemy',
    'sqlalchemy.ext.asyncio',
    'sqlalchemy.orm',
    'alembic',
    'psycopg2-binary',
    'pydantic',
    'pydantic_settings',
    'passlib.context',
    'jose',
    'python-jose',
    'qrcode',
    'pillow',
    'Jinja2',
]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = unittest.mock.MagicMock()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Checkbox-TT'
copyright = '2025, Babenko Vladyslav'
author = 'Babenko Vladyslav'
release = '1.0.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.coverage',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Autodoc configuration --------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Mock imports to avoid dependency issues during doc generation
autodoc_mock_imports = [
    'uvicorn',
    'fastapi',
    'sqlalchemy', 
    'alembic',
    'psycopg2',
    'pydantic',
    'passlib',
    'jose',
    'qrcode',
    'PIL',
    'Jinja2',
    'asyncpg',
    'aiosqlite',
    'bcrypt',
    'email_validator',
    'python_multipart',
    'python_dotenv',
]

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Type hints configuration -----------------------------------------------
always_document_param_types = True
typehints_use_rtype = True
