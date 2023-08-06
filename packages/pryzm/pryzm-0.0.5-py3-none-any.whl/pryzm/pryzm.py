
from pryzm.codes import text_attributes

class Pryzm(object):
    """pz = pryzm.Pryzm(); warn = pz._italic().yellow().red; warn("Achtung!")
        ASCII FORMAT:
            ESC[AT;FG;BGm<text>ESC[0m
    """
    _text_attributes = text_attributes
    def __init__(self, text=None):
        self.text = text if text else ''
        self.at = 0
        self.fg = 30
        self.bg = 40
        self.ASC = u"\u001b["
        self.CLR = u"\u001b[0m"

        for feature, ansi_code in self._text_attributes.items():
            self._add_color(feature, ansi_code)

    def reset(self):
        self.at, self.fg, self.bg = 0, 30, 40
        return self

    def _add_color(self, feature, ansi_code):
        """Add dynamic function to insert color code.
            feature: string, the name of the function to add
            ansi_code: integer, the code value to insert

            return: function, adds a function named 'color' wrapping test with ascii code.
        """
        #print("create {} using {}".format(feature, ansi_code))
        def fn(self, text=None):

            if feature.startswith('_'):
                self.at = ansi_code
            elif feature.isupper():
                self.bg = ansi_code
            elif feature.islower():
                self.fg = ansi_code

            if text:
                self.text = text
                saved_return = self.show()
                print(self.show())
                self.reset()
                return saved_return
            else:
                return self

        setattr(Pryzm, feature, fn)

        fn.__name__ = feature
        fn.__doc__ = "Apply {0} to text".format(feature)

    def show(self):
        return u"{}{};{};{}m{}{}".format(self.ASC, self.at, self.fg, self.bg, self.text, self.CLR)

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
