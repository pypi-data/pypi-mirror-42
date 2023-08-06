# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Nerual network layer"""

from functools import reduce

import numpy as np
from .blob import Tensor, Variable
from .net import sm
from .ops import array_op


class Layer(object):
    """Net is stacked by layers."""

    _auto_name = 0

    def __init__(self, name=None):
        self._name = self._set_name(name)
    

    def _set_name(self, name):
        assert name == None or isinstance(name, str), 'The name of Blob must be string or None, not {}/{}'.format(name, type(name))
        if isinstance(name, str):
            pass
        else:
            name = 'auto_name_' + str(Layer._auto_name)
            Layer._auto_name += 1
        return name

    
    def _add_variable(self, v):
        """Variable will be added to Net for compute grad."""
        return
        if isinstance(v, Variable):
            sm.add_variable(v)
    

    def _add_diff(self, v, diff):
        """If @v is Variable, we need set it's diff."""
        if isinstance(v, Variable):
            v.add_diff(diff)

    
    def _v(self, blob):
        """Get @blob's data"""
        return blob._data

    
    def _inv_v(self, blob, v):
        """Set @blob's data"""
        blob.feed(v)


class Matmul(Layer):
    """TODO(samrsu): Merge bias here"""

    def __init__(self, name='Matmul'):
        super(Matmul, self).__init__(name)

    
    def __call__(self, a, b):
        self._add_variable(a)
        self._add_variable(b)
        res = Tensor()  # res is a tensor, not Variable.
        # You just need @op for tensorflow.
        sm.set_tensor_flow(a, res, lambda :self._op(a=a, b=b, res=res))  # You need not to ser tensorflow for @b to @res, it is duplicate; but remember set gradflow from @res to @b
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, grad=grad))  # invop must need grad
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, grad=grad))
        return res

    
    def _op(self, a, b, res):
        """Layer op, compute output by input
        TODO(smarsu): Deliver numpy data directely.
        
        Args:
            a: Blob
            b: Blob
            res: Result Tensor
        """
        a = a.data
        b = b.data

        res.feed(np.matmul(a, b))

    
    def _compute_diff_b(self, a, b, grad):
        """Compute b's diff
        
        grad: shape like [b, k]
        a: shape like [b, m]
        b: shape like [m, k]
        """
        a = a.data

        a = a.T
        diff = np.matmul(a, grad)

        self._add_diff(b, diff)
        return diff


    def _compute_diff_a(self, a, b, grad):
        """Compute grad for a (lower layer)
        
        grad: shape like [b, k]
        a: shape like [b, m]
        b: shape like [m, k]
        """
        # Note: Here use reshape rather than .T
        # Why both of it can run well
        # TODO(smarsu): Understand it.
        b = b.data

        b = b.T
        #m, k = b.shape
        #b = np.reshape(b, (k, m))
        diff = np.matmul(grad, b)

        self._add_diff(a, diff)
        return diff


matmul = Matmul()


class Add(Layer):
    def __init(self, name='Add'):
        super(Add, self).__init__(name)
    

    def __call__(self, a, b):
        #self.add_variable(a)
        #self.add_variable(b)
        res = Tensor()  # res is a tensor, not Variable.
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, b=b, res=res))  # You need not to ser tensorflow for @b to @res, it is duplicate; but remember set gradflow from @res to @b
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, grad=grad))  # invop must need grad
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, grad=grad))
        return res

    
    def op(self, a, b, res):
        a = a.data
        b = b.data

        res.feed(a + b)

    
    def _compute_diff_a(self, a, b, grad):
        if grad.shape != a.shape:
            grad = np.sum(grad, axis=0)
        diff = grad

        self._add_diff(a, diff)
        return diff

    
    def _compute_diff_b(self, a, b, grad):
        if grad.shape != b.shape:
            grad = np.sum(grad, axis=0)
        diff = grad

        self._add_diff(b, diff)
        return diff


add = Add()


class Multiply(Layer):
    def __init__(self):
        super(Multiply, self).__init__()

    
    def __call__(self, a, b):
        self.add_variable(a)
        self.add_variable(b)
        res = Tensor()  # res is a tensor, not Variable.
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, b=b, res=res))  # You need not to ser tensorflow for @b to @res, it is duplicate; but remember set gradflow from @res to @b
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, grad=grad))  # invop must need grad
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, grad=grad))
        return res

    
    def op(self, a, b, res):
        assert a.shape == b.shape, 'Multiply need @a and @b have the same dim {}/{}'.format(a.shape, b.shape)
        self.inv_v(res, self.v(a) * self.v(b))
    

    def _compute_diff_a(self, a, b, grad):
        assert a.shape == b.shape == grad.shape, 'Multiply need @grad have the save dim with @a'.format(a.shape, b.shape, grad.shape)
        diff = grad * self.v(b)
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff
    

    def _compute_diff_b(self, a, b, grad):
        assert a.shape == b.shape == grad.shape, 'Multiply need @grad have the save dim with @a'.format(a.shape, b.shape, grad.shape)
        diff = grad * self.v(a)
        if isinstance(b, Variable):
            b.add_diff(diff)
        return diff


multiply = Multiply()


class Divide(Layer):
    pass


class Sigmoid(Layer):
    def __init__(self):
        super(Sigmoid, self).__init__()

    
    def __call__(self, a):
        self.add_variable(a)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, res=res))
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, res=res, grad=grad))
        return res

    
    def op(self, a, res):
        self.inv_v(res, array_op.sigmoid(self.v(a)))


    def _compute_diff_a(self, a, res, grad):
        """Calculate grad for lower layer
        
        self._grad: shape like [b, k]
        self._inp: shape like [b, k]
        """
        diff = grad * self.v(res) * (1 - self.v(res))
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff

        self.next_grad = self._grad * self.outp_v() * (1 - self.outp_v())
        return self.next_grad


sigmoid = Sigmoid()


class Relu(Layer):
    def __init__(self):
        super(Relu, self).__init__()

    
    def __call__(self, a):
        self.add_variable(a)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, res=res))
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, grad=grad))
        return res

    
    def op(self, a, res):
        self.inv_v(res, np.maximum(0, self.v(a)))

    
    def _compute_diff_a(self, a, grad):
        tag = np.where(self.v(a)>0, 1, 0)
        diff = grad * tag
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff

    
relu = Relu()


class Tanh(Layer):
    def __init__(self):
        super(Tanh, self).__init__()

    
    def __call__(self, a):
        self.add_variable(a)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, res=res))
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, res=res, grad=grad))
        return res


    def op(self, a, res):
        self.inv_v(res, array_op.tanh(self.v(a)))


    def _compute_diff_a(self, a, res, grad):
        diff = (1 - np.square(self.v(res))) * grad
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff


tanh = Tanh()


class Mse(Layer):
    def __init__(self):
        super(Mse, self).__init__()

    
    def __call__(self, a, b):
        self.add_variable(a)
        self.add_variable(b)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, b=b, res=res))  # Just need tensorflow from a. Note, maybe it will not computed.
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, grad=1))  # Mse is a loss function, the default grad is 1
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, grad=1))
        return res

    
    def op(self, a, b, res):
        # The outp is loss
        self.inv_v(res, 0.5 * np.square(self.v(a) - self.v(b)))

    
    def _compute_diff_a(self, a, b, grad):
        """Compute grad for lower layer

        For this layer, we have no deeper layer's grad
        self._inp: shape like [b, k]
        """
        diff = (self.v(a) - self.v(b)) * grad
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff

        self.next_grad = -(self.label_v() - self.inp_v())
        return self.next_grad

    
    def _compute_diff_b(self, a, b, grad):
        diff = (self.v(b) - self.v(a)) * grad
        if isinstance(b, Variable):
            b.add_diff(diff)
        return diff


mse = Mse()


class _Concat(Layer):
    def __init__(self):
        super(_Concat, self).__init__()

    
    def __call__(self, a, b, axis):
        self.add_variable(a)
        self.add_variable(b)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, b=b, axis=axis, res=res))
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, axis=axis, grad=grad))
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, axis=axis, grad=grad))
        return res
        
    
    def op(self, a, b, axis, res):
        self.inv_v(res, np.concatenate([self.v(a), self.v(b)], axis=axis))
    

    def _compute_diff_a(self, a, b, axis, grad):
        shape_dim = len(grad.shape)
        a_shape = a.shape
        diff = eval(
            'grad[{}{}{}]'.format(
                ''.join([':, '] * (axis % shape_dim)), 
                ':a_shape[axis]', 
                ''.join([':, '] * (shape_dim - axis % shape_dim - 1)),
            )
        )
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff
    

    def _compute_diff_b(self, a, b, axis, grad):
        shape_dim = len(grad.shape)
        a_shape = a.shape
        diff = eval(
            'grad[{}{}{}]'.format(
                ''.join([':, '] * (axis % shape_dim)), 
                'a_shape[axis]:', 
                ''.join([':, '] * (shape_dim - axis % shape_dim - 1)),
            )
        )
        if isinstance(b, Variable):
            b.add_diff(diff)
        return diff


_concat = _Concat()


class Concat(Layer):
    def __init__(self):
        super(Concat, self).__init__()

    
    def __call__(self, blobs, axis):
        return reduce(lambda a, b:_concat(a=a, b=b, axis=axis), blobs)


concat = Concat()


class Slice(Layer):
    def __init__(self):
        super(Slice, self).__init__()

    
    def __call__(self, a, pairs):
        """
        Args:
            a: Tensor
            pairs: str. e.g. '[:, l:r]'
        """
        self.add_variable(a)
        res = Tensor()
        sm.set_tensor_flow()
        sm.set_grad_flow()
        return res

    
    def op(self, a, pairs):
        v_a = self.v(a)
        self.inv_v(res, eval('v_a{}'.format(pairs)))

    
    def _compute_diff_a(self, a, pairs, grad):
        a_shape = self.v(a).shape
        pad_pairs = []
        for s, p in zip(a_shape, pairs):
            if not p:
                pad_pairs.append((0, 0))
            else:
                l, r = p
                assert l >= 0 and r >= 0, 'l, r should bigger than 0.' 
                pad_pairs.append((l, s - r))

        diff = np.pad(grad, pad_pairs, 'constant', constant_values=0)
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff


slice = Slice()


class Embedding_lookup(Layer):
    def __init__(self):
        super(Embedding_lookup, self).__init__()

    
    def __call__(self, idx, weight):
        """Look up @weight at @idx with axis 1.
        
        Args:
            idx: Tensor(), int shape like: [batch, 1] or [batch]
            weight: Tensor(), embedding weight shape like: [num_voca, feature]
        """
        self.add_variable(idx)
        self.add_variable(weight)
        res = Tensor()
        sm.set_tensor_flow(idx, res, lambda :self.op(idx=idx, weight=weight, res=res))
        sm.set_grad_flow(res, weight, lambda grad:self._compute_diff_a(idx=idx, weight=weight, grad=grad))
        return res
    

    def op(self, idx, weight, res):
        idx = self.v(idx)
        weight = self.v(weight)
        idx_shape = idx.shape
        num_voca, feature = weight.shape
        idx = np.reshape(idx, [-1])
        weight = np.concatenate((weight, [[0] * feature]), 0)
        self.inv_v(res, weight[idx])

    
    def _compute_diff_a(self, idx, weight, grad):
        """TODO(smarsu): Remove for loop"""
        idx = self.v(idx)
        num_voca, feature = weight.shape
        diff = np.zeros(weight.shape)
        for grad_idx, weight_idx in enumerate(np.reshape(idx, [-1])):
            if weight_idx >= num_voca: continue
            diff[weight_idx] += grad[grad_idx]
        if isinstance(weight, Variable):
            weight.add_diff(diff)
        return diff


embedding_lookup = Embedding_lookup()


class Softmax_cross_entropy(Layer):
    def __init__(self):
        super(Cross_entropy, self).__init__()
    

    def __call__(self, a, b):
        """
        Args:
            a: Logits.
            b: Labels.
        """
        self.add_variable(a)
        self.add_variable(b)
        res = Tensor()
        sm.set_tensor_flow(a, res, lambda :self.op(a=a, b=b, res=res))  # Just need tensorflow from a. Note, maybe it will not computed.
        sm.set_grad_flow(res, a, lambda grad:self._compute_diff_a(a=a, b=b, grad=1))  # Mse is a loss function, the default grad is 1
        sm.set_grad_flow(res, b, lambda grad:self._compute_diff_b(a=a, b=b, grad=1))
        return res

    
    def op(self, a, b, res):
        a = self.v(a)
        b = self.v(b)
        assert a.shape == b.shape, 'logits should own the same shape with labels'
        a = np.maximum(a, 1e-10)
        self.inv_v(res, -b*np.log(a))

    
    def _compute_diff_a(self, a, b, grad):
        diff = np.where(self.v(a)>1e-10, -self.v(b) / self.v(a) * grad, 0)
        if isinstance(a, Variable):
            a.add_diff(diff)
        return diff


    def _compute_diff_b(self, a, b, grad):
        a = self.v(a)
        a = np.maximum(a, 1e-10)
        diff = -np.log(a) * grad
        if isinstance(b, Variable):
            b.add_diff(diff)
        return diff
