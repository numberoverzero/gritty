import re

CHANNELS = 'rgba'
DEFAULT_COLORS = [0, 0, 0, 255]
CHANNEL_SEARCH = re.compile('[^' + CHANNELS + ']').search
IS_MULTI_CHANNEL = lambda name: len(name) > 1 and not bool(CHANNEL_SEARCH(name))


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
            if hasattr(args[0], '__iter__'):
                args = args[0]
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
            func = lambda (ch, v): setattr(self, ch, v)
            map(func, zip(name, value))
        else:
            object.__setattr__(self, name.lower(), value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Color({})".format(", ".join(str(ch) for ch in self))
