# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Overview nerual network"""

import numpy as np


def Singleton(cls, _instance={}):
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]


    return _singleton


@Singleton
class Net(object):
    """singleton
    
    TODO(smarsu): You can build multi-graph.
    """

    def __init__(self):
        self._tensor_flow = {}
        self._grad_flow = {}
        self._grad_need = {}
        self._tensor_flow_op = []
        self._grad_flow_op = []
        self._variable = set()
        self._variable_momentum = {}
        self._layers = []
        self._layers_data = []
        self._name_layer_map = {}
        self.lr = 1
        pass

    
    def set_tensor_flow(self, a, b, op):
        """Add tensor flow from @a to @b
        
        Args:
            a: Tensor
            b: Tensor
            op: The function to compute @b by @a with other Blobs
        """
        self._tensor_flow_op.append(op)
        self._tensor_flow[a] = self._tensor_flow.get(a, []) + [(b, op)]

    
    def set_grad_flow(self, a, b, op):
        self._grad_flow_op.append(op)
        self._grad_flow[a] = [(b, op)] + self._grad_flow.get(a, [])
        self._grad_need[b] = self._grad_need.get(b, []) + [a]

    
    def add_variable(self, v):
        self._variable.add(v)

    
    def add_layer(self, layer):
        """DEPRECATED
        Add layer to a net.
        
        Args:
            layer: class Layer
        """
        self._layers.append(layer)
        self._layers_data.append([layer._inp, layer, layer._outp])
        self._name_layer_map[layer._name] = layer

    
    def init_all_weight(self):
        for v in self._variable:
            v.random_init()

    
    def _clear_all_weight_diff(self):
        for v in self._variable:
            v.clear_diff()

    
    def _set_feed_dict(self, feed_dict):
        """TODO(smarsu): Complex input and output"""
        for k, v in feed_dict.items():
            k.feed(v)
        return 


        self._layers[0]._inp.feed(feed_dict['data_x'])
        self._layers[-1]._label.feed(feed_dict['data_y'])
        self.lr = feed_dict['lr']

    
    def _grad_merge(self, stack):
        """grad need different op"""
        tmp = {}
        for b, grad, cnt in stack:
            if b in tmp:
                # grad 0
                tmp[b][0] += grad
                # cnt 1
                tmp[b][1] += cnt
            else:
                tmp[b] = [grad, cnt]
        stack = [[b, grad, cnt] for b, (grad, cnt) in tmp.items()]
        return stack

    
    def forward(self, feed_dict=None):
        if feed_dict is None: feed_dict = {}
        self._set_feed_dict(feed_dict)  # put data_x, data_y on shallow and deep layer
        for op in self._tensor_flow_op:
            op()
        return 

        for layer in self._layers:
            layer.op()
        return self._layers[-1].outp_v(), self._layers[-2].outp_v()

    
    def optimize(self, blob, grad, lr=0.1):
        """@blob must be a single Blob.
        Here is the last layer's @grad should divided by @batch_size
        
        TODO(smarsu): Change @stack to dict so than we don't need merge.
        """
        stack = [[blob, grad * lr, 0]] # for b, op in self._grad_flow[blob]] # add 0 for count 
        while stack:
            new_stack = []
            for b, grad, cnt in stack:
                if cnt == len(self._grad_need.get(b, [])):
                    #next_grad = op(grad)
                    new_stack += [[_b, _op(grad), 1] for _b, _op in self._grad_flow.get(b, [])]
                else:
                    new_stack.append([b, grad, cnt])
            stack = new_stack
            stack = self._grad_merge(stack)
        return


    def optimize_bak(self, blob, grad=1):
        stack = [[b, op, grad] for b, op in self._grad_flow[blob]]
        while stack:
            new_stack = []
            for b, op, grad in stack:
                next_grad = op(grad)
                new_stack += [[_b, _op, next_grad] for _b, _op in self._grad_flow.get(b, [])]
            stack = new_stack
        return

        grads = []
        for b, op in self._grad_flow[blob]:
            grad = op(grad)
            grads.append(grad)
        for (b, op), grad in zip(self._grad_flow[blob], grads):
            return 
    

    def _momentum_update(self):
        """Reference: Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour
        
        Ut+1 = m * Ut + grad
        Wt+1 = Wt - lr * Ut+1
        """
        for v in self._variable:
            self._variable_momentum[v] = v.add_diff(self._momentum * self._variable_momentum.get(v, 0))

    
    def update(self, momentum=0.):
        """Calculate grad from deep layer to shallow layer
        Here @lr affect the grad about every weight in the net. ? Is that true?
        
        Should update before compute next grad?
        TODO(smarsu): Multi branch net
                      Check out why @momentum affect the converge. 
                      Can we merge the momentum into the prime grad. -> No. Because Tensor() or Variable() changed.
        """
        self._momentum = momentum

        self._momentum_update()

        for v in self._variable:
            v.update()
        
        for v in self._variable:
            v.clear_diff()
        return

        next_grad = None
        print('layer:', self._layers[::-1])
        for layer in self._layers[::-1]:
            layer.set_grad(next_grad)
            next_grad = layer.cal_next_grad()
            #print(next_grad)
            #layer.update(self.lr)
            #next_grad = layer.cal_next_grad()
            #print(next_grad)
        
        for layer in self._layers[::-1]:
            layer.update(self.lr)
        
        for layer in self._layers[::-1]:
            layer.clear()

    
sm = Net()
