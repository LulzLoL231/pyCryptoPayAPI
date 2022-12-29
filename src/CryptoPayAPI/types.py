# -*- coding: utf-8 -*-
# For backward compatibility
import warnings

from .schemas import *


warnings.warn(
    '"CryptoPayAPI.types" name is deprecated, use "CryptoPayAPI.schemas" instead!',
    DeprecationWarning, stacklevel=2
)
