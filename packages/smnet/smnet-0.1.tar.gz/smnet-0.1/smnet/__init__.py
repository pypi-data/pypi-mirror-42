from .blob import *
from . import layer as nn
from .net import *

init_all_weight = sm.init_all_weight
forward = sm.forward
optimize = sm.optimize
update = sm.update

from .layers import *
