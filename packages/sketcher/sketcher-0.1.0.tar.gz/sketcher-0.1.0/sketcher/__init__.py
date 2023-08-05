from .backend import get_backend
from .common import Color, Shape
import random
import math
from .config import Config

name = "sketcher"

config = Config()


class Sketch:
    def __init__(self):
        if not hasattr(self, 'Backend'):
            self.Backend = get_backend()

    def start(self):
        self.can = self.Backend()
        self.can.init()
        self.can.start(self.setup, self.loop)

    def clear(self):
        self.can.clear()

    def frame(self, l):
        self.can.set_frame(l)

    def fill(self):
        self.can.set_fill(True)

    def no_fill(self):
        self.can.set_fill(False)

    def stroke(self):
        self.can.set_stroke(True)

    def no_stroke(self):
        self.can.set_stroke(False)

    def fill_color(self, col):
        self.can.set_fill_color(col)

    def stroke_color(self, col):
        self.can.set_stroke_color(col)

    def mouse_state(self):
        return self.can.get_mouse_state()

    def keyboard_state(self, ):
        return self.can.get_keyboard_state()

    def size(self, w, h):
        self.can.set_size(w, h)

    def background(self, color):
        self.can.set_background(Color(color))

    def shape(self, shape):
        if not isinstance(shape, Shape):
            shape = Shape(list(shape))
        self.can.draw_shape(shape)

    def point(self, x, y):
        self.can.draw_point(x, y)

    def line(self, x1, y1, x2, y2):
        self.can.draw_line(x1, y1, x2, y2)

    def rectangle(self, x, y, w, h=None):
        if h is None:
            h = w
        self.can.draw_rectangle(x, y, w, h)

    def ellipse(self, x, y, a, b=None):
        if b is None:
            b = a
        self.can.draw_ellipse(x, y, a, b)

    def text(self, x, y, text, **kwargs):
        self.can.draw_text(x, y, text, **kwargs)

    def image(self, x, y, image):
        self.can.draw_image(x, y, image)

    def refresh(self):
        self.can.refesh()


Sketch.m = math
Sketch.rd = random

try:
    import numpy
    Sketch.np = numpy
except ImportError:
    Sketch.np = None


def sketch(sk):
    if issubclass(sk, Sketch):
        MySketch = sk
    else:
        class MySketch(Sketch, sk):
            pass
    MySketch.Backend = get_backend(config.backend_use)
    MySketch.__name__ = sk.__name__
    MySketch().start()
    return MySketch
