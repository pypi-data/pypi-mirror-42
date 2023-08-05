"""
Base file for the dqm_compute module.
"""

from . import config

from .compute import compute, compute_procedure
from .config import get_config
from .stock_mols import get_molecule

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
