
import sys
import time

from subprocess import Popen, PIPE
from pryzm.codes import cap27, text_attributes

class Pryzm(object):
    """
        ASCII FORMAT:
            ESC[AT;FG;AT;BGm<text>ESC[0m
    """
    _cap27 = cap27
    _text_attributes = text_attributes
    def __init__(self, text=None):
        self.text = text if text else ''
        self.subject = text
        self.at = 1
        self.fg = 30
        self.bg = 40
        self.CLR = u"\u001b[0m"

        for key, val in self._text_attributes.items():
            self._add_color(key, val)

    def _add_color(self, color, code):
        """Add dynamic function to insert color code.
            color: string, the name of the function to add
            value: integer, the code value to insert
            return: function, adds a function named 'color' wrapping test with ascii code.
        """
        def fn(self, text=None):
            if text: self.text = text
            if code >= 40:
                self.bg = code
            elif code >= 30:
                self.fg = code
            elif code <= 10:
                self.at = code
            print(code)
            return self

        setattr(Pryzm, color, fn)

        fn.__name__ = color
        fn.__doc__ = "Apply {0} to text".format(color)

    def show(self):
        return u"\u001b[{};{};1;{}m{}{}".format(self.at, self.fg, self.bg, self.text, self.CLR)

    def print(self):
        print(self.show())

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
