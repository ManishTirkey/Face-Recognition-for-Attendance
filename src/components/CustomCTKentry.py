from typing import List, Callable, Tuple, Optional, Union

import customtkinter as ctk
from src.components.Register_style import Styling


# copy of the class inside test_2.py
class CTKCustomEntry(ctk.CTkEntry, Styling):
    def __init__(self, master):
        ctk.CTkEntry.__init__(self, master=master)
        Styling.__init__(self)

        self._frame = self
        self.configure(border_color=self.border_color,
                       border_width=self.border_width,
                       fg_color=self.entry_bg_color)

        self.bind("<FocusIn>", lambda e: self.__focusIn())
        self.bind("<FocusOut>", lambda e: self.__focusOut())

    def __focusIn(self, callback=None):
        # print(f"focusIn")
        self.configure(border_color=self.focus_in_border_color)

        if callback is not None:
            callback(self)

    def __focusOut(self, callback=None):
        # print(f"focusOut")
        self.configure(border_color=self.border_color)

        if callback is not None:
            callback(self)

    def __Changing(self):
        self.configure(border_color=self.border_color)
        self.unbind("<Key>")

    # callback focus IN/OUT
    def focus_in(self, callback=None) -> None:
        self.bind("<FocusIn>", lambda e: self.__focusIn(callback))

    def focus_out(self, callback=None) -> None:
        self.bind("<FocusOut>", lambda e: self.__focusOut(callback))

    def KeyChange(self):
        self.bind("<Key>", lambda e: self.__Changing())


class CustomCombobox(ctk.CTkComboBox, Styling):
    def __init__(self, master, values: List[str]):
        self.values = values

        self.entry_height: int = 40
        self.combobox_height: int = 40
        self.radius: int = 50

        Styling.__init__(self)
        ctk.CTkComboBox.__init__(self, master=master, values=self.values)

        self.configure(height=self.combobox_height,
                       corner_radius=self.radius,
                       state='readonly',
                       border_width=2,
                       border_color=self.combbx_bd_color,
                       )
        self.set(self.values[0])

    def current(self, index):
        try:
            if index < len(self.values):
                ...
        except:
            raise IndexError("index value is out of boundaries")
        else:
            self.set(self.values[index])


class CustomButton(ctk.CTkButton):
    btn_count = 1

    def __init__(self, master, onEnter, onLeave):
        CustomButton.btn_count += 1
        text = f"Button-{CustomButton.btn_count}"

        ctk.CTkButton.__init__(self, master=master, text=text)

        self.bind("<Enter>", lambda e: self.Enter(e, onEnter))
        self.bind("<Leave>", lambda e: self.Leave(e, onLeave))

    @staticmethod
    def Enter(event, callback):
        event.widget.configure(cursor="hand2")
        if callback is not None:
            callback(event)

    @staticmethod
    def Leave(event, callback):
        event.widget.configure(cursor="")
        if callback is not None:
            callback(event)


class Component_lb_en(ctk.CTkFrame, Styling):
    def __init__(self, parent,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None
                 ):
        Styling.__init__(self)

        ctk.CTkFrame.__init__(self, master=parent)

        if fg_color is None:
            # if fg_color is none then inherit from parent
            parent_color = parent.cget("fg_color")
            self.configure(fg_color=parent_color)
        else:
            self.configure(fg_color=fg_color)

        self.pack(side=ctk.TOP, fill=ctk.X, expand=True, pady=(0, 20))

        # self._frame = self

        self.entry_height: int = 40
        self.combobox_height: int = 40
        self.radius: int = 50

    def __Label(self) -> ctk.CTkLabel:
        label = ctk.CTkLabel(self)
        label.configure(anchor="w",
                        corner_radius=self.radius,
                        text_color=self.label_text_color,
                        )
        label.pack(side=ctk.TOP,
                   fill=ctk.X,
                   expand=False)
        return label

    def Label(self, **kwargs) -> ctk.CTkLabel:
        label = self.__Label()
        label.configure(**kwargs)
        return label

    def __Entry(self) -> CTKCustomEntry:
        entry = CTKCustomEntry(self)
        entry.configure(height=self.entry_height,
                        corner_radius=self.radius)
        entry.pack(side=ctk.TOP, fill=ctk.X, expand=False)

        return entry

    def Entry(self, **kwargs) -> CTKCustomEntry:
        entry = self.__Entry()
        entry.configure(**kwargs)
        return entry

    def __Button(self, **kwargs) -> ctk.CTkButton:
        btn = CustomButton(self, **kwargs)
        # btn = ctk.CTkButton(self)
        btn.configure(height=self.entry_height,
                      corner_radius=8,
                      )
        btn.pack(side=ctk.TOP, fill=ctk.X, expand=True)

        return btn

    def Button(self, onEnter: Callable[[], None] = None, onLeave: Callable[[], None] = None, **kwargs) -> ctk.CTkButton:
        btn = self.__Button(onEnter=onEnter, onLeave=onLeave)
        btn.configure(**kwargs)
        return btn

    def Combobox(self, combobox_values: List[str], **kwargs) -> ctk.CTkComboBox:
        combobox = CustomCombobox(self, values=combobox_values)
        combobox.pack(side=ctk.TOP, fill=ctk.X, expand=True)
        combobox.configure(**kwargs)
        return combobox

    # def __getattr__(self, attr):
    #     return getattr(self._frame, attr)
