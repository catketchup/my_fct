import numpy as np
import matplotlib.pyplot as plt

from sotodlib import core
import sotodlib.io.load as io_load

from moby2.analysis import socompat
socompat.register_loaders()

from sotodlib.core import FlagManager
import sotodlib.flags as flags
import sotodlib.sim_flags as sim_flags

import sotodlib.tod_ops.filters as filters
from sotodlib.tod_ops import fourier_filter, rfft, detrend_data

import tools
import importlib
importlib.reload(tools)
from tools import in_range
