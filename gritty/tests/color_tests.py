import unittest
from gritty.color import Color, CHANNELS, DEFAULT_COLORS


def with_defaults(*args, **kwargs):
    colors = list(DEFAULT_COLORS)
    if args:
        for i, v in enumerate(args):
            colors[i] = v
    else:
        for ch, v in kwargs.iteritems():
            index = CHANNELS.index(ch)
            colors[index] = v
    return colors


class ColorTests(unittest.TestCase):

    def test_init_iterable(self):
        it = [0, 1, 2, 255]
        color = Color(it)
        print color
        assert with_defaults(*it) == list(color)

    def test_copy_init(self):
        args = [0, 1, 2, 255]
        color = Color(*args)
        color2 = Color(color)
        assert with_defaults(*args) == list(color2)

    def test_init_args(self):
        args = [0, 1, 2, 255]
        color = Color(*args)
        assert with_defaults(*args) == list(color)

    def test_init_partial_args(self):
        args = [0, 1, 2]
        color = Color(*args)
        assert with_defaults(*args) == list(color)

    def test_init_kwargs(self):
        kwargs = {'a': 3, 'b': 2, 'g': 1, 'r': 0}
        color = Color(**kwargs)
        assert with_defaults(**kwargs) == list(color)

    def test_init_partial_kwargs(self):
        kwargs = {'a': 3, 'r': 0}
        color = Color(**kwargs)
        assert with_defaults(**kwargs) == list(color)

    def test_single_channel_access(self):
        kwargs = {'r': 0, 'g': 1, 'b': 2, 'a': 3}
        color = Color(**kwargs)
        for ch, v in kwargs.iteritems():
            assert getattr(color, ch) == v

    def test_multiple_channel_access(self):
        args = [0, 1, 2, 3]
        color = Color(*args)
        assert color.rg == [0, 1]

    def test_multichannel_ordering(self):
        args = [0, 1, 2, 3]
        color = Color(*args)
        assert color.rgba == [0, 1, 2, 3]
        assert color.rbga == [0, 2, 1, 3]
        assert color.abgr == [3, 2, 1, 0]

    def test_multichannel_assignment(self):
        color = Color()
        assert color.ra == [0, 255]
        color.ra = [1, 254]
        assert color.ra == [1, 254]

    def test_multichannel_swap(self):
        color = Color()
        assert color.ba == [0, 255]
        color.ba = color.ab
        assert color.ba == [255, 0]
