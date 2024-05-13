import re

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

from src.components.CustomCTKentry import Component_lb_en
from src.components.Register_style import Styling

from public.DB import *


class forget_password(ctk.CTkToplevel, Styling):
    def __init__(self, parent, title):
        ctk.CTkToplevel.__init__(self, parent)
        Styling.__init__(self)

        self.conn = Connect()
        self.cursor = None

        self.table_name = title

        self.titl = title.capitalize()
        self.title(self.titl + " Forget Password")
        width = 1200
        height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window position
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.update_idletasks()
        self.grab_set()
        self.transient(parent)

        self.title_font = ("Ubuntu", 32, "bold")
        self.main_container = Component_lb_en(self)
        self.main_container.configure(corner_radius=10)
        self.main_container.pack(fill=ctk.BOTH, padx=50, pady=50)

        self.build()

        self.protocol("WM_DELETE_WINDOW", self.Destroy)
        self.bind("<Return>", lambda e: self.ReturnBinding())

    def Destroy(self):
        self.unbind("<Return>")
        Disconnect(self.conn)
        self.destroy()

    def ReturnBinding(self):
        if self.new_btn._state == "normal":
            self.update_password()

        elif self.fp_btn._state == "normal":
            self.Check_in_DB()

    def build(self):
        self.build_left()
        self.build_right()

    def build_left(self):
        distance = 8

        title_container = Component_lb_en(self.main_container)
        title_container.configure(fg_color=self.title_bg_color,
                                  corner_radius=10
                                  )
        title_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, ipadx=100, pady=0)

        who = ctk.CTkLabel(title_container)
        who.configure(text=self.titl,
                      anchor=ctk.W,
                      text_color=self.title_color,
                      font=self.title_font)
        who.pack(fill=ctk.X, anchor=ctk.W, padx=10, pady=(100, distance))

        for_title = ctk.CTkLabel(title_container, text="Forget",
                                 anchor=ctk.W,
                                 text_color=self.title_color,
                                 font=self.title_font)
        for_title.pack(fill=ctk.X, anchor=ctk.W, padx=10, pady=(0, distance))

        pass_title = ctk.CTkLabel(title_container,
                                  text="Password",
                                  anchor=ctk.W,
                                  text_color=self.title_color,
                                  font=self.title_font)
        pass_title.pack(fill=ctk.X, anchor=ctk.W, padx=10)

    def build_right(self):
        # * email validate registry
        # vcmd = (self.register(self.Email_validate_callback), '%P')
        # ivcmd = (self.register(self.Email_invalid),)

        self.t_pady = (40, 0)
        self.b_pady = (30, 10)
        self.radius = 50
        self.height = 40
        self.bg_color = ("#DADADA", "#2F2F2F")
        self.divider_color = ("#D4D4D4", "#383838")

        content_container = Component_lb_en(self.main_container)
        content_container.configure(corner_radius=10,
                                    border_width=1)
        content_container.pack(fill=ctk.BOTH, pady=0)

        heading = ctk.CTkLabel(content_container,
                               text="Change Your Password")
        heading.pack(side=ctk.TOP, fill=ctk.X, pady=(40, 0), padx=10)

        content_wrapper = Component_lb_en(content_container)
        content_wrapper.pack(fill=ctk.X, expand=False, pady=(50, 0), padx=10)

        address_container = Component_lb_en(content_wrapper)
        address_container.pack(side=ctk.LEFT,
                               fill=ctk.BOTH,
                               padx=10,
                               pady=self.t_pady)
        self.address = address_container.Entry(placeholder_text="Enter you email")

        self.fp_btn = address_container.Button(text="Forget Password", command=self.Check_in_DB)
        self.fp_btn.pack(pady=self.b_pady)

        self.msg_email = Component_lb_en.Label(address_container)
        self.msg_email.configure(text=" ", anchor="center")
        self.msg_email.pack(pady=self.b_pady)

        divider = ctk.CTkFrame(content_wrapper,
                               fg_color=self.divider_color,
                               width=2)
        divider.pack(side=ctk.LEFT, fill=ctk.Y)

        new_container = Component_lb_en(content_wrapper)
        new_container.pack(side=ctk.RIGHT,
                           fill=ctk.BOTH,
                           padx=10,
                           pady=self.t_pady)

        self.new = new_container.Entry(placeholder_text="New Passcode")

        self.confirm = new_container.Entry(placeholder_text="Confirm New Passcode")
        self.confirm.pack(pady=self.b_pady)

        self.new_btn = new_container.Button(text="Change Password", command=self.update_password)
        self.new_btn.pack(pady=self.b_pady)
        self.Password_disable()

        self.msg_new = new_container.Label(text=" ")
        self.msg_new.configure(text_color=self.SUCCESS, anchor="center")
        self.msg_new.pack(pady=self.b_pady)

    def Password_enable(self):
        self.fp_btn.configure(state="disabled")
        self.new.configure(state="normal")
        self.new.focus()
        self.confirm.configure(state="normal")
        self.new_btn.configure(state="normal")

        self.address.configure(state="disabled")

    def Password_disable(self):
        self.address.configure(state="normal")
        self.fp_btn.configure(state="normal")

        self.new.configure(state="normal")
        self.confirm.configure(state="normal")

        self.new.delete(0, ctk.END)
        self.confirm.delete(0, ctk.END)

        self.new.configure(placeholder_text="New Passcode")
        self.confirm.configure(placeholder_text="Confirm New Passcode")

        self.new.configure(state="disabled")
        self.confirm.configure(state="disabled")
        self.new_btn.configure(state="disabled")

    def update_password(self):
        new = self.new.get().strip(" ")
        confirm = self.confirm.get().strip(" ")
        if len(new) == 0 or len(confirm) == 0 or new != confirm:
            self.new.configure(border_color=self.ERROR)
            self.confirm.configure(border_color=self.ERROR)
            self.msg_new.configure(text="Password Mismatching",
                                   text_color=self.ERROR)
            return

        self.new.configure(border_color=self.border_color)
        self.confirm.configure(border_color=self.border_color)

        try:
            email = self.address.get().strip(" ")
            query = f"""
                UPDATE {self.table_name} SET PASSWORD=%s WHERE EMAIL=%s
            """
            values = (confirm, email, )

            self.cursor = Execute(self.conn, query, values)

            self.msg_new.configure(text="Changed Successfully",
                                   text_color=self.SUCCESS)
            self.Password_disable()
            self.address.focus()

        except Exception as e:
            self.msg_new.configure(text="an error occurred",
                                   text_color=self.ERROR)
            CTkMessagebox(self, title="Error", message=f"{e}", icon="cancel")

        else:
            # Initiate the facial_registration
            ...

    def Check_in_DB(self):
        email = self.address.get().strip(" ")
        if len(email) == 0:
            self.address.configure(border_color=self.ERROR)
            return

        self.address.configure(border_color=self.border_color)

        query = f"""select id from {self.table_name} WHERE EMAIL=%s"""
        values = (email, )

        try:
            self.cursor = Execute_Fetch(self.conn, query, values)
            data = self.cursor.fetchone()

        except Exception as e:
            print(e)
            self.msg_email.configure(text="No Found User's Email",
                                     text_color=self.ERROR
                                     )
        else:

            if data is not None:
                self.msg_email.configure(text="Found User's Email",
                                         text_color=self.SUCCESS
                                         )
                self.Password_enable()

                self.msg_new.configure(text="Set Your Password",
                                       text_color="white"
                                       )
            else:
                self.msg_email.configure(text="Not Found User's Email",
                                         text_color=self.ERROR
                                         )

    # def Email_validate_callback(self, value):
    #     """validate the email entry
    #     :param value:
    #     :return:
    #     """
    #     pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    #     if re.fullmatch(pattern, value) is None:
    #         self.msg_email.configure(text="Incorrect Email Id | Type Error",
    #                                  text_color="#E74C3C")
    #         return False
    #
    #     return True
    #
    # def Email_invalid(self):
    #     """show the error message if the data is not valid
    #     :return:
    #     """
    #     self.msg_email.configure(text="Invalid Email address | Try again",
    #                              text_color="#E74C3C")
    #
    # # event handling
    #
    # def Verify_password(self) -> bool:
    #     """
    #     checks both new and confirm passwords
    #     :return:
    #     """
    #     return self.new_password == self.confirm_password
    #
    # def Verify_email(self) -> bool:
    #     """
    #     verify with database if already exists or not
    #     :return:
    #     """
    #     if self.email is not None:  # and self.email == db_email
    #         return True
    #     print("verifying email")
    #     return False
    #
    # def Update_passcode(self):
    #     """
    #     update password if Verify_email is success
    #     :return:
    #     """
    #     # self.Verify_email()
    #     # self.Verify_password()
    #
    #     self.Show()
    #
    # def Show(self):
    #     print(self.email, self.new_password, self.confirm_password)


if __name__ == '__main__':
    app = ctk.CTk()
    forget_password(app, 'student')
    app.mainloop()
