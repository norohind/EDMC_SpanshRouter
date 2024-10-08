from tkinter import Entry, END, StringVar

from config import config


class PlaceHolder(Entry):
    def __init__(self, parent, placeholder, **kw):
        if parent is not None:
            Entry.__init__(self, parent, **kw)
        self.var = self["textvariable"] = StringVar()
        self.placeholder = placeholder
        self.placeholder_color = "grey"

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        if self.get() != self.placeholder:
            self.set_text(self.placeholder, True)

    def set_text(self, text, placeholder_style=True):
        if placeholder_style:
            self['fg'] = self.placeholder_color
        else:
            self.set_default_style()
        self.delete(0, END)
        self.insert(0, text)

    def force_placeholder_color(self):
        self['fg'] = self.placeholder_color

    def set_default_style(self):
        theme = config.get_int('theme')
        self['fg'] = config.get_str('dark_text') if theme else "black"

    def set_error_style(self, error=True):
        if error:
            self['fg'] = "red"
        else:
            self.set_default_style()

    def foc_in(self, *args):
        if self['fg'] == "red" or self['fg'] == self.placeholder_color:
            self.set_default_style()
            if self.get() == self.placeholder:
                self.delete('0', 'end')

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
