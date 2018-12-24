from ._version import __version_info__, __version__
from .alzw import (
    compress as alzw_compress,
    decompress as alzw_decompress,
)

__all__ = [
    '__version_info__',
    '__version__',
    'alzw_compress',
    'alzw_decompress',
]