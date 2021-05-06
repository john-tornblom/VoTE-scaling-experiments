import ctypes
import ctypes.util
import os


ctypes.CDLL(ctypes.util.find_library('stdc++'), mode=ctypes.RTLD_GLOBAL)
lib = ctypes.CDLL((os.path.dirname(__file__) or '.') + '/libnnet.so')

lib.load_network.restype = ctypes.c_void_p
lib.load_network.argtypes = [ctypes.c_char_p]

lib.destroy_network.restype = None
lib.destroy_network.argtypes = [ctypes.c_void_p]

lib.num_inputs.restype = ctypes.c_int
lib.num_inputs.argtypes = [ctypes.c_void_p]

lib.num_outputs.restype = ctypes.c_int
lib.num_outputs.argtypes = [ctypes.c_void_p]

lib.is_symmetric.restype = ctypes.c_int
lib.is_symmetric.argtypes = [ctypes.c_void_p]

lib.input_max.restype = ctypes.c_int
lib.input_max.argtypes = [ctypes.c_void_p, ctypes.c_uint]

lib.input_min.restype = ctypes.c_int
lib.input_min.argtypes = [ctypes.c_void_p, ctypes.c_uint]

lib.input_mean.restype = ctypes.c_int
lib.input_mean.argtypes = [ctypes.c_void_p, ctypes.c_uint]

lib.input_range.restype = ctypes.c_int
lib.input_range.argtypes = [ctypes.c_void_p, ctypes.c_uint]

lib.output_mean.restype = ctypes.c_int
lib.output_mean.argtypes = [ctypes.c_void_p]

lib.output_range.restype = ctypes.c_int
lib.output_range.argtypes = [ctypes.c_void_p]

lib.evaluate_network.restype = ctypes.c_int
lib.evaluate_network.argtypes = [ctypes.c_void_p,
                                 ctypes.POINTER(ctypes.c_double),
                                 ctypes.POINTER(ctypes.c_double),
                                 ctypes.c_bool, ctypes.c_bool]


class NeuralNetwork(object):
    ptr = None
    _normalize_input = False
    _normalize_output = False
    
    def __init__(self, filename,
                 normalize_input=True,
                 normalize_output=True):

        self._normalize_input = normalize_input
        self._normalize_output = normalize_output
        self.ptr = lib.load_network(filename.encode('ascii'))
        assert self.ptr
        
    def __del__(self):
        if lib:
            lib.destroy_network(self.ptr)

    @property
    def input_dims(self):
        return lib.num_inputs(self.ptr)

    @property
    def output_dims(self):
        return lib.num_outputs(self.ptr)

    @property
    def is_symmetric(self):
        return lib.is_symmetric(self.ptr)

    @property
    def input_min(self):
        return [lib.input_min(self.ptr, index)
                for index in range(self.input_dims)]

    @property
    def input_max(self):
        return [lib.input_max(self.ptr, index)
                for index in range(self.input_dims)]

    @property
    def input_mean(self):
        return [lib.input_mean(self.ptr, index)
                for index in range(self.input_dims)]

    @property
    def input_range(self):
        return [lib.input_range(self.ptr, index)
                for index in range(self.input_dims)]

    @property
    def output_mean(self):
        return lib.output_mean(self.ptr)

    @property
    def output_range(self):
        return lib.output_range(self.ptr)

    def normalize_input(self, invec):
        
        def normalize_value(val, minval, maxval, mean, var):
            if val > maxval: return (maxval - mean) / var
            if val < minval: return (minval - mean) / var
            return (val - mean) / var

        return [normalize_value(val, minval, maxval, mean, var)
                for val, minval, maxval, mean, var
                in zip(invec, self.input_min, self.input_max,
                       self.input_mean, self.input_range)]

    def normalize_output(self, outvec):
        return [val*self.output_range + self.output_mean
                for val in outvec]
    
    def evaluate(self, invec):
        invec = (ctypes.c_double * self.input_dims)(*invec)
        outvec = (ctypes.c_double * self.output_dims)()
        
        lib.evaluate_network(self.ptr, invec, outvec,
                             self._normalize_input,
                             self._normalize_output)

        return list(outvec)

    def predict(self, X):
        return [self.evaluate(x) for x in X]

