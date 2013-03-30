

class NotifiableDict(dict):
    def __init__(self, iterable=None, **kwargs):
        if iterable is None:
            iterable = []
        dict.__init__(self, iterable, **kwargs)
        self._notify_func = lambda *a, **kw: None

    def set_notify_func(self, func):
        '''func should take 3 arguments: key, old_value, new_value'''
        self._notify_func = func

    def __setitem__(self, key, value):
        old_value = self.get(key, None)
        dict.__setitem__(self, key, value)
        self._notify_func(key, old_value, value)

    def __delitem__(self, key):
        old_value = self.get(key, None)
        dict.__delitem__(self, key)
        self._notify_func(key, old_value, None)
