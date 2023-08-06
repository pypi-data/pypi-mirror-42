# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Reccurent nerual network layer"""

import numpy as np
from ..blob import Tensor, Variable
from .. import layer as nn

class Rnn(nn.Layer):
    def __init__(self):
        super(Rnn, self).__init__()

    
    def __call__(self, inputs, state, hidden_size=None, input_size=None):
        """
        Args:
            inputs: List of Tensor(), e.g. [Tensor(), ..., Tensor()]
                Every times input of RNN.
            state: The initial state of RNN, in default, it should be zeros.
            hidden_size: The hidden units size of RNN.
        Returns:
            outputs:
            states:
        """
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        weight = Variable((hidden_size + input_size, hidden_size))
        bias = Variable((hidden_size, ))
        outputs = []
        states = []
        for inp in inputs:
            output, state = self.op(inp, state, weight, bias)
            outputs.append(output)
            states.append(state)
        return outputs, states


    def op(self, inp, state, weight, bias):
        """TODO(smarsu): Add bias to matmul"""
        data_x = nn.concat([inp, state], axis=-1)
        data_y = nn.add(nn.matmul(data_x, weight), bias)
        data_y = nn.tanh(data_y)
        return data_y, data_y  # Note: Did here need duplicate?


rnn = Rnn()


class Lstm(nn.Layer):
    def __init__(self):
        super(Lstm, self).__init__()

    
    def __call__(self, inputs, state, hidden_size=None, input_size=None, forget_bias=1.):
        """TODO(smarsu): One matmul; initializers.glorot_uniform()
        """
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        w1 = Variable((hidden_size + input_size, hidden_size))
        b1 = Variable((hidden_size, ))
        w2 = Variable((hidden_size + input_size, hidden_size))
        b2 = Variable((hidden_size, ))
        w3 = Variable((hidden_size + input_size, hidden_size))
        b3 = Variable((hidden_size, ))
        w4 = Variable((hidden_size + input_size, hidden_size))
        b4 = Variable((hidden_size, ))
        outputs = []
        states = []
        for inp in inputs:
            output, state = self.op(inp, state, w1, b1, w2, b2, w3, b3, w4, b4, forget_bias)
            outputs.append(output)
            states.append(state)
        return outputs, states

    
    def op(self, inp, state, w1, b1, w2, b2, w3, b3, w4, b4, forget_bias):
        c, h = state
        data_x = nn.concat([inp, h], -1)
        f = nn.add(nn.matmul(data_x, w1), b1)
        i = nn.sigmoid(nn.add(nn.matmul(data_x, w2), b2))
        j = nn.tanh(nn.add(nn.matmul(data_x, w3), b3))
        o = nn.sigmoid(nn.add(nn.matmul(data_x, w4), b4))
        forget_bias = Tensor(v=np.ones_like(f._data) * forget_bias)
        f = nn.sigmoid(nn.add(f, forget_bias))
        new_c = nn.add(
            nn.multiply(c, f),
            nn.multiply(i, j),
        )
        new_h = nn.multiply(o, nn.tanh(new_c))
        return new_h, (new_c, new_h)


lstm = Lstm()
