
from pryzm import text_attributes

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
        self.features = []
        self.ASC = u"\u001b["
        self.CLR = u"\u001b[0m"

        for feature, ansi_code in self._text_attributes.items():
            self._add_color(feature, ansi_code)

    def reset(self):
        self.features = []
        return self

    def _add_color(self, feature, ansi_code, show=True):
        """Add dynamic function to insert color code.
            feature: string, the name of the function to add
            ansi_code: integer, the code value to insert

            return: function, adds a function named 'color' wrapping test with ascii code.
        """
        def fn(self, text=None):
            self.features.append(str(ansi_code))

            if text:
                self.text = text
                saved_return = self.show()
                if show: print(self.show())
                self.reset()
                if show:
                    return saved_return
                else:
                    return
            else:
                return self

        setattr(Pryzm, feature, fn)

        fn.__name__ = feature
        fn.__doc__ = "Apply {0} to text".format(feature)

    def show(self):
        return u"{}{}m{}{}".format(self.ASC, ";".join(self.features), self.text, self.CLR)

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
