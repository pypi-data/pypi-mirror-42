#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = persis.persis:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import pkgutil


__author__ = "Martin Skarzynski"
__copyright__ = "Martin Skarzynski"
__license__ = "MIT"


def get_df_pkl(path: str = 'data/df.pkl'):
    """Access data included with the package
    Returns:
        Pickled pandas dataframe
    """
    return pkgutil.get_data('persis', path)


def get_model_pkl(path: str = 'models/knn.pkl'):
    """Access a model included with the package
    Returns:
        Scikit-learn model picked with joblib

    """
    return pkgutil.get_data('persis', path)
