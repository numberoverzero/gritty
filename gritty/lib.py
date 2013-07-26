# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify gritty. If modification is your
# game, it is recommended that you read the GNU LGPL license:
# http://www.gnu.org/licenses/
import re
import collections


def coerce_alpha(input, *args, **kwargs):
    '''Default to full opacity'''
    return Color(input)


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


CHANNELS = 'rgba'
DEFAULT_COLORS = [0, 0, 0, 255]
CHANNEL_SEARCH = re.compile('[^' + CHANNELS + ']').search
IS_MULTI_CHANNEL = lambda name: name and not bool(CHANNEL_SEARCH(name))


class Color(object):
    '''
    Access color channels by index or value.
    Full channel swizzling is supported, including setters

    # Set rgba to (50, 100, 150, 200)
    color = Color(50, 100, 150, 200)

    # Flip red and green channels
    color.rg = color.gr

    # Add green to red (index order is rgba)
    color[0] += color.g
    '''
    __slots__ = list(CHANNELS)

    def __init__(self, *args, **kwargs):
        self[:] = DEFAULT_COLORS

        if args:
            self[:len(args)] = args
        else:
            for (ch, default) in zip(CHANNELS, DEFAULT_COLORS):
                setattr(self, ch, kwargs.get(ch, default))

    def __iter__(self):
        return iter(getattr(self, CHANNELS))

    def __len__(self):
        return len(CHANNELS)

    def __getitem__(self, index):
        return getattr(self, CHANNELS[index])

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            index = range(*index.indices(len(CHANNELS)))
            func = lambda (i, v): setattr(self, CHANNELS[i], v)
            map(func, zip(index, value))
        else:
            setattr(self, CHANNELS[index], value)

    def __getattr__(self, name):
        if IS_MULTI_CHANNEL(name):
            return list(getattr(self, ch) for ch in name)
        return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if IS_MULTI_CHANNEL(name):
            func = lambda ch, v: setattr(self, ch, v)
            map(func, zip(name, value))
        else:
            object.__setattr__(self, name.lower(), value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Color({})".format(", ".join(str(ch) for ch in self))
