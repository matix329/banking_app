import os
import sys
sys.path.insert(0, os.path.abspath('../banking_core'))

project = 'banking_app'
copyright = '2024, Mateusz Siejo'
author = 'Mateusz Siejo'
release = '1.3.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']