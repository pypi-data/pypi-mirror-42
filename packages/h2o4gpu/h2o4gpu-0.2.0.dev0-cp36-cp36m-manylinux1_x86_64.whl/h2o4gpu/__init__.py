# pylint: skip-file
"""
:copyright: 2017 H2O.ai, Inc.
:license:   Apache License Version 2.0 (see LICENSE for details)
"""
#Skip pylint b / c this is automatically concatenated at compile time
#with other init files
# TODO: grab this from BUILD_INFO.txt or __about__.py
__version__ = "0.2.0"

DAAL_SUPPORTED=True

try:
    __import__('daal')
except ImportError:
    DAAL_SUPPORTED=False

if DAAL_SUPPORTED:
    from .solvers.daal_solver.regression import Method as LinearMethod
from .types import FunctionVector
from .solvers.pogs import Pogs
from .solvers.elastic_net import ElasticNet
from .solvers.elastic_net import ElasticNetH2O
from .solvers.logistic import LogisticRegression
from .solvers.linear_regression import LinearRegression
from .solvers.lasso import Lasso
from .solvers.ridge import Ridge
from .solvers.xgboost import RandomForestRegressor
from .solvers.xgboost import RandomForestClassifier
from .solvers.xgboost import GradientBoostingClassifier
from .solvers.xgboost import GradientBoostingRegressor
from .solvers.kmeans import KMeans
from .solvers.kmeans import KMeansH2O
from .solvers.pca import PCA
from .solvers.pca import PCAH2O
from .solvers.truncated_svd import TruncatedSVD
from .solvers.truncated_svd import TruncatedSVDH2O
from .typecheck import typechecks
from .typecheck import compatibility
from . import h2o4gpu_exceptions
from .util import metrics
from .util import import_data
"""
Machine learning module for Python
==================================

h2o4gpu is a Python module integrating classical machine
learning algorithms in the tightly-knit world of scientific Python
packages (numpy, scipy, matplotlib).

It aims to provide simple and efficient solutions to learning problems
that are accessible to everybody and reusable in various contexts:
machine-learning as a versatile tool for science and engineering.

See http://h2o4gpu.org for complete documentation.
"""
import sys
import re
import warnings
import os
from contextlib import contextmanager as _contextmanager
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

_ASSUME_FINITE = bool(os.environ.get('SKLEARN_ASSUME_FINITE', False))


def get_config():
    """Retrieve current values for configuration set by :func:`set_config`

    Returns
    -------
    config : dict
        Keys are parameter names that can be passed to :func:`set_config`.
    """
    return {'assume_finite': _ASSUME_FINITE}


def set_config(assume_finite=None):
    """Set global h2o4gpu configuration

    Parameters
    ----------
    assume_finite : bool, optional
        If True, validation for finiteness will be skipped,
        saving time, but leading to potential crashes. If
        False, validation for finiteness will be performed,
        avoiding error.
    """
    global _ASSUME_FINITE
    if assume_finite is not None:
        _ASSUME_FINITE = assume_finite


@_contextmanager
def config_context(**new_config):
    """Context manager for global h2o4gpu configuration

    Parameters
    ----------
    assume_finite : bool, optional
        If True, validation for finiteness will be skipped,
        saving time, but leading to potential crashes. If
        False, validation for finiteness will be performed,
        avoiding error.

    Notes
    -----
    All settings, not just those presently modified, will be returned to
    their previous values when the context manager is exited. This is not
    thread-safe.

    Examples
    --------
    >>> import h2o4gpu
    >>> from h2o4gpu.utils.validation import assert_all_finite
    >>> with h2o4gpu.config_context(assume_finite=True):
    ...     assert_all_finite([float('nan')])
    >>> with h2o4gpu.config_context(assume_finite=True):
    ...     with h2o4gpu.config_context(assume_finite=False):
    ...         assert_all_finite([float('nan')])
    ... # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: Input contains NaN, ...
    """
    old_config = get_config().copy()
    set_config(**new_config)

    try:
        yield
    finally:
        set_config(**old_config)


# Make sure that DeprecationWarning within this package always gets printed
warnings.filterwarnings('always', category=DeprecationWarning,
                        module=r'^{0}\.'.format(re.escape(__name__)))

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#



try:
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of h2o4gpu when
    # the binaries are not built
    __SKLEARN_SETUP__
except NameError:
    __SKLEARN_SETUP__ = False

if __SKLEARN_SETUP__:
    sys.stderr.write('Partial import of h2o4gpu during the build process.\n')
    # We are not importing the rest of the scikit during the build
    # process, as it may not be compiled yet
else:
    from . import __check_build
    from .base import clone
    __check_build  # avoid flakes unused variable error

    __all__ = ['calibration', 'cluster', 'covariance', 'cross_decomposition',
               'cross_validation', 'datasets', 'decomposition', 'dummy',
               'ensemble', 'exceptions', 'externals', 'feature_extraction',
               'feature_selection', 'gaussian_process', 'grid_search',
               'isotonic', 'kernel_approximation', 'kernel_ridge',
               'learning_curve', 'linear_model', 'manifold', 'metrics',
               'mixture', 'model_selection', 'multiclass', 'multioutput',
               'naive_bayes', 'neighbors', 'neural_network', 'pipeline',
               'preprocessing', 'random_projection', 'semi_supervised',
               'svm', 'tree', 'discriminant_analysis',
               # Non-modules:
               'clone']


def setup_module(module):
    """Fixture for the tests to assure globally controllable seeding of RNGs"""
    import os
    import numpy as np
    import random

    # It could have been provided in the environment
    _random_seed = os.environ.get('SKLEARN_SEED', None)
    if _random_seed is None:
        _random_seed = np.random.uniform() * (2 ** 31 - 1)
    _random_seed = int(_random_seed)
    print("I: Seeding RNGs with %r" % _random_seed)
    np.random.seed(_random_seed)
    random.seed(_random_seed)
