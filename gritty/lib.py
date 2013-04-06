# Copyright 2013 Joe Cross
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify gritty. If modification is your
# game, it is recommended that you read the GNU LGPL license:
# http://www.gnu.org/licenses/
import re


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

_channels = 'rgba'
_channel_defaults = [0, 0, 0, 255]
_channel_search = re.compile('[^' + _channels + ']').search
_multi_channel = lambda name: len(name) > 1 and not bool(_channel_search(name))


class Color(object):
    __slots__ = list(_channels)

    def __init__(self, *args, **kwargs):
        if len(args) > 1 and len(kwargs) > 1:
                raise TypeError("Cannot specify color using both positional and keyword arguments")

        # Set defaults
        self[:] = _channel_defaults

        if args:
            # This check allows us to load values from any iterable
            if len(args) == 1 and hasattr(args[0], '__iter__'):
                args = args[0]
            colors = list(args)
            self[:len(colors)] = colors
        else:
            for ch, v in kwargs.iteritems():
                if ch in _channels:
                    setattr(self, ch, v)

    def __iter__(self):
        return iter(getattr(self, _channels))

    def __len__(self):
        return len(getattr(self, _channels))

    def __getitem__(self, index):
        return list(self)[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            index = range(*index.indices(len(_channels)))
        else:
            index = [index]

        if hasattr(value, '__iter__'):
            ni, nv = len(index), len(value)
            if nv != ni:
                raise AttributeError("Tried to set {} channels but passed {} values".format(ni, nv))
        else:
            value = [value]
        func = lambda (i, v): setattr(self, _channels[i], v)
        map(func, zip(index, value))

    def __getattr__(self, name):
        if _multi_channel(name):
            return list(getattr(self, ch) for ch in name)
        return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if _multi_channel(name):
            func = lambda ch, v: setattr(self, ch, v)
            map(func, zip(name, value))
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Color({})".format(", ".join(str(ch) for ch in self))
