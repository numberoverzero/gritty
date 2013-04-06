# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify gritty. If modification is your
# game, it is recommended that you read the GNU LGPL license:
# http://www.gnu.org/licenses/
import re


def coerce_alpha(input, *args, **kwargs):
    '''Default to full opacity'''
    if len(input) == 3:
        input = list(input)
        input.append(255)
    return input


class NotifiableDict(dict):
    def __init__(self, iterable=None, **kwargs):
        iterable = iterable or []
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

_rgba = 'rgba'
_channel_search = re.compile('[^rgba]').search
_multi_channel = lambda name: len(name) > 1 and not bool(_channel_search(name))


class Color(object):
    __slots__ = ['r', 'g', 'b', 'a']

    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __iter__(self):
        return iter(self.rgba)

    def __getitem__(self, index):
        return list(self)[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            indices = range(*index.indices(4))
        else:
            indices = [index]
        func = lambda i: setattr(self, _rgba[i], value)
        map(func, indices)

    def __getattr__(self, name, oga):
        if _multi_channel(name):
            return list(object.__getattr__(self, ch) for ch in name)
        return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if _multi_channel(name):
            func = lambda ch, v: object.__setattr__(self, ch, v)
            map(func, zip(name, value))
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Color({}, {}, {}, {})".format(*self)
