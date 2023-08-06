from time import time

class UnassignedValue(object):
    pass

class ThrottledSource(object):

    def __init__(self, callback, timeout):
        self.cb = callback
        self.timeout = timeout
        self.time = time()
        self.value = UnassignedValue()

    def timed_out(self):
        return time() > self.timeout+self.time

    def get(self):
        if isinstance(self.value, UnassignedValue) or self.timed_out():
            print("Value timed out, calling {}".format(self.cb.__name__))
            self.value = self.cb()
            self.time = time()
        return self.value

class ConstantSource(object):

    def __init__(self, callback):
        self.cb = callback
        self.value = UnassignedValue()

    def get(self):
        if isinstance(self.value, UnassignedValue):
            self.value = self.cb()
        return self.value
