# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Data block, with tensor and variable"""

import numpy as np

from .net import sm


class Blob(object):
    """Data stored by numpy."""

    _auto_name = 0

    def __init__(self, name=None, _type='Blob'):
        self._data = None
        self._diff = None
        self._shape = None

        self._type = _type
        self._name = self._set_name(name)

    
    def _set_name(self, name):
        assert name == None or isinstance(name, str), 'The name of Blob must be string or None, not {}/{}'.format(name, type(name))
        if isinstance(name, str):
            pass
        else:
            name = 'auto_name_' + str(Blob._auto_name)
            Blob._auto_name += 1
        return '/'.join([self._type, name])

    
    def _set_shape(self, shape):
        self._shape = shape

    
    def feed(self, v):
        self._data = np.array(v)  # A copy of v
        self._set_shape(self._data.shape)  # Blob's shape is changable with it's data
    

    @property
    def shape(self):
        return self._shape

    
    @property
    def data(self):
        return self._data

    
    @property
    def diff(self):
        return self._diff

    
    @property
    def name(self):
        return self._name


class Variable(Blob):
    def __init__(self, value=None, shape=None, name=None):
        """TODO(smarsu): If both @value and @shape not be None, shape we check the @value's shape equal to @shape"""
        assert not(value is None and shape is None), '@value and @shape can not both be None'
        super(Variable, self).__init__(name, _type='Variable')
        sm.add_variable(self)  # Variable should be added into Net for compute grad.
        if shape is not None:
            self._set_shape(shape)
        if value is not None:
            self.feed(value)
        self._diff = 0  # It is quick to use 0 rather than np.zeros(shape)

    
    def random_init(self):
        """For variable have not been given certain value, we should random init it."""
        if isinstance(self._shape, int) or len(self._shape) == 1:
            # For bias, we need zero init
            self._data = np.zeros(self._shape)
        else:
            self._data = np.random.normal(-0.01, 0.01, self._shape)

    
    def restore(self, value):
        self.feed(value)

    
    def add_diff(self, diff):
        assert isinstance(diff, float) or diff.shape == self._shape, 'the shape of grad is not match the shape of Variable: {}/{}'.format(diff.shape, self._shape)
        self._diff += diff  # Use `+=` rather than `=` can haddle merge multi grad.
        return self._diff
    

    def clear_diff(self):
        """You should clear grad after update."""
        self._diff = 0

    
    def update(self, lr=1):
        """Update weights

        Should lr be here?
        Args:
            Deprate: @lr: learning rate.
            @lr has been merged into the prime grad.
        """
        self._data -= self._diff


class Tensor(Blob):
    def __init__(self, value=None, shape=None, name=None):
        super(Tensor, self).__init__(name, _type='Tensor')
        if shape is not None:
            self._set_shape(shape)
        if value is not None:
            self.feed(value)
