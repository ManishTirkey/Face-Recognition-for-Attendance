from tkinter import *

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from PIL import Image
import os
import re

from public.DB import *
from public.file_config import Component_img
from src.components.Register_style import Styling
from src.components.CustomCTKentry import Component_lb_en

from src.components import Teacher_Dashboard as TD
from src.components import Student_Dashboard as SD


class Login(ctk.CTkToplevel, Styling):
    def __init__(self, parent, title):
        self.parent = parent

        ctk.CTkToplevel.__init__(self, master=self.parent)
        Styling.__init__(self)

        try:
            self.conn = Connect()
        except Exception as e:
            CTkMessagebox(parent, title="Error", message=f"Initialize your database first", icon="cancel")
            return

        self.cursor = None

        self.table_name = title
        self.titl = title.capitalize()

        self.title(self.titl + " Login Form")
        width = 1200
        height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position center of window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window position
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)
        self.update_idletasks()
        self.grab_set()
        self.transient(parent)

        self.t_pady = (80, 10)
        self.b_pady = (30, 10)

        # main container holds everything
        self.main_container = Component_lb_en(self)
        self.main_container.configure(corner_radius=8, border_width=1, border_color=self.frame_border_color)
        self.main_container.pack(fill=ctk.BOTH, padx=50, pady=50)

        self.build()

        self.protocol("WM_DELETE_WINDOW", self.Destroy)
        self.bind("<Return>", lambda e: self.Validate())

    def Destroy(self):
        self.email_entry.unbind("<FocusIn>")
        self.password_entry.unbind("<FocusIn>")
        self.unbind("<Return>")

        Disconnect(self.conn, self.cursor)
        self.destroy()

    def build(self) -> None:
        self.build_left()
        self.build_right()

    def build_left(self) -> None:
        """
        contains all the elements of left side
        :return:
        """

        title_container = Component_lb_en(self.main_container)
        title_container.configure(fg_color=self.title_bg_color,
                                  corner_radius=10)
        title_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, ipadx=100, pady=4, padx=4)

        who = title_container.Label(text=self.titl,
                                    anchor=ctk.W,
                                    text_color=self.title_color,
                                    font=self.title_font)
        who.pack(fill=ctk.X, anchor=ctk.W, padx=10, pady=(100, self.distance))

        for_title = title_container.Label(text="Login",
                                          anchor=ctk.W,
                                          text_color=self.title_color,
                                          font=self.title_font)
        for_title.pack(fill=ctk.X, anchor=ctk.W, padx=10, pady=(0, self.distance))

    def build_right(self) -> None:
        """
        contains all the elements of right side
        it's split into two sub child
        :return:
        """
        self.content_container = Component_lb_en(self.main_container)
        self.content_container.configure(corner_radius=10)
        self.content_container.pack(side=ctk.RIGHT, fill=ctk.BOTH, pady=4, padx=4)

        self.content_left()

    def content_left(self) -> None:
        """
        left form
        :return:
        """

        content_right_frame = Component_lb_en(self.content_container)
        content_right_frame.pack(padx=10, pady=self.t_pady)
        if self.titl.lower() == "teacher":
            text = "Email"
            placeholder = "example123@gmail.com"
        else:
            text = "Roll No. / Email address"
            placeholder = "Roll No. / example123@gmail.com"

        email = Component_lb_en(content_right_frame)
        email.Label(text=text)
        self.email_entry = email.Entry(placeholder_text=placeholder)

        password = Component_lb_en(content_right_frame)
        password.Label(text="Password")
        self.password_entry = password.Entry(placeholder_text="Password", show="*")

        icon = Image.open(os.path.join(Component_img, "reg_512.png"))
        icon = ctk.CTkImage(icon, size=(25, 25))

        login_btn = Component_lb_en(content_right_frame)
        login_btn.pack(pady=(20, 10))
        self.new_btn = login_btn.Button(text="Login", image=icon, compound="right",
                                        corner_radius=8,
                                        command=self.Validate)

        status = Component_lb_en(content_right_frame)
        self.msg = status.Label(text="", anchor="center")

    def Reset(self):
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)


    def Validate(self):
        txt = self.email_entry.get()
        s_pass = self.password_entry.get()
        query = ""

        if self.CheckEmail(txt):
            # check if txt is email or not, if True then validate with email and password
            query = f"""
            SELECT id FROM {self.table_name} WHERE EMAIL=%s AND PASSWORD=%s
            """

        else:
            # txt is roll no, so validate with db

            if self.titl.lower() == 'student' and txt.isnumeric():
                query = f"""
                SELECT id FROM {self.table_name} WHERE ROLL=%s AND PASSWORD=%s
                """

            else:
                self.email_entry.configure(border_color=self.ERROR)
                self.password_entry.configure(border_color=self.ERROR)
                self.msg.configure(text="Wrong Login details.",
                                   text_color=self.ERROR)
                return

        try:
            values = (txt, s_pass)
            self.cursor = Execute_Fetch(self.conn, query, values)
            s_id = self.cursor.fetchone()
        except:
            s_id = None

        if s_id is None:
            self.email_entry.configure(border_color=self.ERROR)
            self.password_entry.configure(border_color=self.ERROR)
            self.msg.configure(text="Wrong Login details.",
                               text_color=self.ERROR)
            return

        self.email_entry.configure(border_color=self.border_color)
        self.password_entry.configure(border_color=self.border_color)
        self.msg.configure(text="Login Successfully.",
                           text_color=self.SUCCESS)
        s_id = s_id[0]
        if self.table_name == 'teacher':
            TD.Dashboard(self.parent, s_id)

        elif self.table_name == 'student':
            SD.Dashboard(self.parent, s_id)

        self.after(200, lambda: self.Destroy())

    @staticmethod
    def CheckEmail(txt):
        pattern = r'^[a-zA-Z0-9_]+@gmail\.com$'
        regex = re.compile(pattern)

        if regex.match(txt):
            return True
        return False


if __name__ == '__main__':
    app = ctk.CTk()
    Login(app, 'student')
    app.mainloop()
    