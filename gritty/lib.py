# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify gritty. If modification is your
# game, it is recommended that you read the GNU LGPL license:
# http://www.gnu.org/licenses/


def coerce_alpha(input, *args, **kwargs):
    '''Default to full opacity'''
    if len(input) == 3:
        input = list(input)
        input.append(255)
    return input


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
