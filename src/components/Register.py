import tkinter as tk
from tkinter import *
from tkcalendar import *

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from PIL import Image, ImageTk
import re
import os
from typing import List, Tuple
from threading import Thread

from public.file_config import Gender, Security_questions, Departments, Semesters, IMAGE_FOLDER, Component_img
from public.DB import *
from src.components.DATETIME import Date
from src.components.Register_style import Styling
from src.components.CustomCTKentry import Component_lb_en
from src.Id_generator import SnowflakeGenerator as sfg
from src.Register_face import Take_image


class Student_data:
    def __int__(self):
        self.roll_entry = None
        self.name_entry = None
        self.gender_combbx = None
        self.dept_combbx = None
        self.sem_combbx = None

        self.email_entry = None
        self.ph_entry = None
        self.password_entry = None
        self.confirm_pass_entry = None
        self.sec_combbx = None
        self.security_entry = None


class Student_Register(ctk.CTkToplevel, Styling):
    def __init__(self, parent, title="Student"):
        ctk.CTkToplevel.__init__(self, master=parent)
        Styling.__init__(self)

        try:
            self.conn = Connect()
        except Exception as e:
            CTkMessagebox(self, title="Error", message=f"Initialize your database first", icon="cancel")
            return

        self.cursor = None

        self.data = Student_data()

        self.titl = title
        self.title(self.titl + " Registration Form")
        width = 1200
        height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position t751430
        # o center window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window position
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)
        self.update_idletasks()
        self.grab_set()
        self.transient(parent)

        self.t_pady = (30, 10)
        self.b_pady = (30, 10)

        # main container holds everything
        self.main_container = Component_lb_en(self)
        self.main_container.configure(corner_radius=10,
                                      border_width=1,
                                      border_color=self.frame_border_color)
        self.main_container.pack(fill=ctk.BOTH, padx=50, pady=50)

        self.build()

        self.bind("<Return>", lambda e: self.register_data())
        self.protocol("WM_DELETE_WINDOW", self.Destroy)

    def Destroy(self):
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
        title_container.configure(fg_color=self.title_bg_color, corner_radius=10)
        title_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, ipadx=100, pady=4, padx=4)

        who = title_container.Label(text=self.titl,
                                    anchor=ctk.W,
                                    text_color=self.title_color,
                                    font=self.title_font)
        who.pack(anchor=ctk.W, padx=10, pady=(100, self.distance))

        for_title = title_container.Label(text="Registrations",
                                          anchor=ctk.W,
                                          text_color=self.title_color,
                                          font=self.title_font)
        for_title.pack(anchor=ctk.W, padx=10, pady=(0, self.distance))

    def build_right(self) -> None:
        """
        contains all the elements of right side
        it's split into two sub child
        :return:
        """
        self.content_wrapper = Component_lb_en(self.main_container)
        self.content_wrapper.configure(corner_radius=10)
        self.content_wrapper.pack(side=ctk.RIGHT, fill=ctk.BOTH, pady=4, padx=4)

        self.content_left()
        self.content_right()

    def content_left(self) -> None:
        """
        left form
        :return:
        """
        content_left_frame = Component_lb_en(self.content_wrapper)
        content_left_frame.pack(side=ctk.LEFT,
                                fill=ctk.BOTH,
                                padx=10,
                                pady=self.t_pady)

        roll = Component_lb_en(content_left_frame)
        roll.Label(text="Roll Number")
        self.data.roll_entry = roll.Entry(placeholder_text="Roll Number", state="disabled")
        self.Roll_no_check_db()

        name = Component_lb_en(content_left_frame)
        name.Label(text="Full Name")
        self.data.name_entry = name.Entry(placeholder_text="Full Name")

        date = Component_lb_en(content_left_frame)
        date.Label(text="Date of Birth")
        date.Button(text=f"{Date()}").configure(anchor='w',
                                                text_color=("#797979", "#797979"),
                                                border_width=self.border_width,
                                                corner_radius=50,
                                                fg_color=self.entry_bg_color,
                                                hover=False,
                                                border_color=self.border_color
                                                )

        gender = Component_lb_en(content_left_frame)
        gender.pack(pady=(0, 6))
        gender.Label(text="Gender")
        gender_values = [i for i in Gender]
        self.data.gender_combbx = gender.Combobox(combobox_values=gender_values)

        dept = Component_lb_en(content_left_frame)
        dept.pack(pady=(0, 6))
        dept.Label(text="Department")
        deprt_values = [i for i in Departments]
        self.data.dept_combbx = dept.Combobox(combobox_values=deprt_values)

        sem = Component_lb_en(content_left_frame)
        sem.pack(pady=(0, 6))
        sem.Label(text="Semester")
        sem_values = [i for i in Semesters]
        self.data.sem_combbx = sem.Combobox(combobox_values=sem_values)

    def content_right(self) -> None:
        """
        right form
        :return:
        """

        content_right_frame = Component_lb_en(self.content_wrapper)
        content_right_frame.pack(side=ctk.RIGHT,
                                 fill=ctk.BOTH,
                                 padx=10,
                                 pady=self.t_pady)

        email = Component_lb_en(content_right_frame)
        email.Label(text="Email address *")
        self.data.email_entry = email.Entry(placeholder_text="example123@gmail.com")

        ph = Component_lb_en(content_right_frame)
        ph.Label(text="Phone Number")
        self.data.ph_entry = ph.Entry(placeholder_text="Phone Number.")

        new_password = Component_lb_en(content_right_frame)
        new_password.Label(text="New Password *")
        self.data.password_entry = new_password.Entry(placeholder_text="New Password")

        confirm_pass = Component_lb_en(content_right_frame)
        confirm_pass.Label(text="Confirm New Password *")
        self.data.confirm_pass_entry = confirm_pass.Entry(placeholder_text="Confirm New Password", show="*")

        security = Component_lb_en(content_right_frame)
        security.Label(text="Security Questions *")
        values = [i for i in Security_questions]

        self.data.sec_combbx = security.Combobox(combobox_values=values)
        self.data.sec_combbx.pack(pady=(0, 5))
        self.data.security_entry = security.Entry(placeholder_text="Enter secrit answer")

        icon = Image.open(os.path.join(Component_img, "reg_512.png"))
        icon = ctk.CTkImage(icon, size=(25, 25))

        self.new_btn = ctk.CTkButton(content_right_frame,
                                     command=self.register_data,
                                     text="New Registration",
                                     image=icon,
                                     compound="right",
                                     corner_radius=8
                                     )
        self.new_btn.pack(side=ctk.TOP, fill=ctk.X, pady=(20, 10))

    def Roll_no_check_db(self):
        self.data.roll_entry.delete(0, ctk.END)
        query = """
            SELECT MAX(ROLL) AS roll FROM student; 
            """

        row = Execute_Fetch(self.conn, query)
        roll_no = row.fetchone()[0]

        if roll_no is not None:
            roll_no += 1
        else:
            roll_no = 1

        self.data.roll_entry.configure(state="normal")
        self.data.roll_entry.delete(0, ctk.END)
        self.data.roll_entry.insert(0, roll_no)
        self.data.roll_entry.configure(state="disabled")

    def Callback_focusOut(self, obj):
        if self.Verify_password():
            self.data.password_entry.configure(border_color=self.border_color)
            self.data.confirm_pass_entry.configure(border_color=self.border_color)
        else:
            self.data.password_entry.configure(border_color=self.ERROR)
            self.data.confirm_pass_entry.configure(border_color=self.ERROR)

    def register_data(self):
        name = self.data.name_entry.get()
        gender = self.data.gender_combbx.get()
        department = self.data.dept_combbx.get()
        semester = self.data.sem_combbx.get()

        email = self.data.email_entry.get()
        phone = self.data.ph_entry.get()
        password = self.data.password_entry.get()
        confirm_password = self.data.confirm_pass_entry.get()
        secret_question = self.data.sec_combbx.get()
        secret_answer = self.data.security_entry.get()

        # --------------------------------------------inner function
        def Register_data(stu_id):

            # insert data to database
            try:
                query = """
                    INSERT INTO student (
                        id, EMAIL, NAME, PHONE, DEPARTMENT, SEMESTER, GENDER, 
                        PASSWORD, SECRET_QUESTION, SECRET_ANSWER
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                values = (stu_id, email, name, phone, department,
                          semester, gender, confirm_password,
                          secret_question, secret_answer
                          )
                self.cursor = Execute(self.conn, query, values)

                self.after(500, lambda: self.main_container.configure(border_color=self.SUCCESS))
                self.after(3000, lambda: self.main_container.configure(border_color=self.frame_border_color))


            except Exception as e:
                CTkMessagebox(self, title="Error", message=f"{e}", icon="cancel")

            else:
                # resetting all input
                self.Roll_no_check_db()

                self.data.name_entry.delete(0, ctk.END)
                self.data.email_entry.delete(0, ctk.END)
                self.data.ph_entry.delete(0, ctk.END)
                self.data.password_entry.delete(0, ctk.END)
                self.data.confirm_pass_entry.delete(0, ctk.END)
                self.data.security_entry.delete(0, ctk.END)

                self.data.gender_combbx.current(0)
                self.data.dept_combbx.current(0)
                self.data.sem_combbx.current(0)
                self.data.sec_combbx.current(0)

        # ------------------------------------close inner function

        try:
            if not self.Verify_password():

                self.data.password_entry.focus()

                self.data.password_entry.configure(border_color=self.ERROR)
                self.data.confirm_pass_entry.configure(border_color=self.ERROR)

                self.data.password_entry.unbind("<FocusIn>")
                self.data.confirm_pass_entry.unbind("<FocusIn>")

                self.data.password_entry.KeyChange()
                self.data.confirm_pass_entry.KeyChange()

                self.data.password_entry.unbind("<FocusOut>")
                self.data.confirm_pass_entry.unbind("<FocusOut>")

                self.data.password_entry.focus_out(callback=self.Callback_focusOut)
                self.data.confirm_pass_entry.focus_out(callback=self.Callback_focusOut)

                raise ValueError("password is not matching with confirm password")

            else:
                self.data.password_entry.configure(border_color=self.border_color)
                self.data.confirm_pass_entry.configure(border_color=self.border_color)

            if len(secret_answer.strip(" ")) == 0:
                self.data.security_entry.unbind("<FocusIn>")
                self.data.security_entry.KeyChange()
                self.data.security_entry.focus()
                self.data.security_entry.configure(border_color=self.ERROR)
                raise ValueError("enter the secret answer.")

        except Exception as e:
            # CTkMessagebox(self, title="Error", message=f"{e}", icon="cancel")
            ...

        else:
            s_id = sfg(node_id=1).generate_id()
            # face Register
            register = Thread(target=Take_image, daemon=False, args=(IMAGE_FOLDER, s_id, Register_data))
            register.start()

    def Verify_password(self) -> bool:
        passw = self.data.password_entry.get().strip(" ")
        cpass = self.data.confirm_pass_entry.get().strip(" ")

        if len(passw) != 0 and len(cpass) != 0 and passw == cpass:
            return True
        return False

    # def check_password(self):


class Teacher_Data:
    def __int__(self):
        self.Id_entry = None
        self.name_entry = None
        self.email_entry = None
        self.gender_combbx = None
        self.dept_combbx = None

        self.password_entry = None
        self.confirm_pass_entry = None
        self.sec_comb = None
        self.security_entry = None


class Teacher_Register(ctk.CTkToplevel, Styling):
    def __init__(self, parent, title="Teacher"):
        ctk.CTkToplevel.__init__(self, master=parent)
        Styling.__init__(self)

        try:
            self.conn = Connect()
        except Exception as e:
            CTkMessagebox(self, title="Error", message=f"Initialize your database first", icon="cancel")
            return

        self.cursor = None
        self.data = Teacher_Data()

        self.titl = title
        self.title(self.titl + " Registration Form")
        width = 1200
        height = 700

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position t751430
        # o center window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window position
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)
        self.update_idletasks()
        self.grab_set()
        self.transient(parent)

        self.bg_color = ("#DADADA", "#2F2F2F")
        self.radius = 50
        self.t_pady = (40, 10)
        self.b_pady = (30, 10)
        self.height = 40

        # main container holds everything
        self.main_container = Component_lb_en(self)
        self.main_container.configure(corner_radius=10, border_width=1,
                                      border_color=self.frame_border_color)
        self.main_container.pack(fill=ctk.BOTH, padx=50, pady=50)

        self.build()

        self.bind("<Return>", lambda e: self.register_data())
        self.protocol("WM_DELETE_WINDOW", self.Destroy)

    def Destroy(self):
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
                                  corner_radius=10,
                                  )
        title_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=False, ipadx=100, pady=4, padx=4)

        who = title_container.Label()
        who.configure(text=self.titl,
                      anchor=ctk.W,
                      text_color=self.title_color,
                      font=self.title_font)
        who.pack(fill=ctk.X, anchor=ctk.W, padx=10, pady=(100, self.distance))

        for_title = title_container.Label(text="Registrations",
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
        self.content_wrapper = Component_lb_en(self.main_container)
        self.content_wrapper.pack(side=ctk.RIGHT, fill=ctk.BOTH, pady=60, padx=2)

        self.content_left()

        # divider = Component_lb_en(self.content_wrapper)
        # divider.configure(fg_color=self.divider_color,
        #                   width=2)
        # divider.pack(side=ctk.LEFT, fill=ctk.Y, pady=(20, 20))

        self.content_right()

    def content_left(self) -> None:
        """
        left form
        :return:
        """
        content_left_frame = Component_lb_en(self.content_wrapper)
        content_left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=10,
                                pady=self.t_pady)

        # Id = Component_lb_en(content_left_frame)
        # Id.Label(text="Teacher's Id")
        # self.data.Id_entry = Id.Entry(placeholder_text="Teacher's  Id")

        name = Component_lb_en(content_left_frame)
        name.Label(text="Full Name")
        self.data.name_entry = name.Entry(placeholder_text="Full Name")

        email = Component_lb_en(content_left_frame)
        email.Label(text="Email address *")
        self.data.email_entry = email.Entry(placeholder_text="example123@gmail.com")

        gender = Component_lb_en(content_left_frame)
        gender.pack(pady=(0, 6))
        gender.Label(text="Gender")
        gender_values = [i for i in Gender]
        self.data.gender_combbx = gender.Combobox(combobox_values=gender_values)

        dept = Component_lb_en(content_left_frame)
        dept.pack(pady=(0, 6))
        dept.Label(text="Department")
        deprt_values = [i for i in Departments]
        self.data.dept_combbx = dept.Combobox(combobox_values=deprt_values)

    def content_right(self) -> None:
        """
        right form
        :return:
        """

        content_right_frame = Component_lb_en(self.content_wrapper)
        content_right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=10,
                                 pady=self.t_pady)

        password = Component_lb_en(content_right_frame)
        password.Label(text="New Password *")
        self.data.password_entry = password.Entry(placeholder_text="New Password")

        confirm_pass = Component_lb_en(content_right_frame)
        confirm_pass.Label(text="Confirm New Password *")
        self.data.confirm_pass_entry = confirm_pass.Entry(placeholder_text="Confirm New Password",
                                                          show="*"
                                                          )

        security = Component_lb_en(content_right_frame)
        security.Label(text="Security Questions *")
        values = [i for i in Security_questions]
        self.data.sec_comb = security.Combobox(combobox_values=values)
        self.data.sec_comb.pack(pady=(0, 5))
        self.data.security_entry = security.Entry(placeholder_text="Enter secrit answer.")

        icon = Image.open(os.path.join(Component_img, "reg_512.png"))
        icon = ctk.CTkImage(icon, size=(25, 25))

        self.new_btn = ctk.CTkButton(content_right_frame,
                                     text="New Registration",
                                     command=self.register_data,
                                     image=icon,
                                     compound="right",
                                     corner_radius=8)
        self.new_btn.pack(side=ctk.TOP, fill=ctk.X, pady=self.b_pady)

    def Callback_focusOut(self, obj):
        print("callback called")
        if self.Verify_password():
            self.data.password_entry.configure(border_color=self.border_color)
            self.data.confirm_pass_entry.configure(border_color=self.border_color)

        else:
            self.data.password_entry.configure(border_color=self.ERROR)
            self.data.confirm_pass_entry.configure(border_color=self.ERROR)

    def register_data(self):
        name = self.data.name_entry.get()
        email = self.data.email_entry.get()
        gender = self.data.gender_combbx.get()
        department = self.data.dept_combbx.get()

        # password = self.data.password_entry.get()
        confirm_password = self.data.confirm_pass_entry.get()
        security_question = self.data.sec_comb.get()
        security_answer = self.data.security_entry.get()

        try:

            if not self.Verify_password():

                self.data.confirm_pass_entry.focus()

                self.data.password_entry.configure(border_color=self.ERROR)
                self.data.confirm_pass_entry.configure(border_color=self.ERROR)

                self.data.password_entry.unbind("<FocusIn>")
                self.data.confirm_pass_entry.unbind("<FocusIn>")

                self.data.password_entry.KeyChange()
                self.data.confirm_pass_entry.KeyChange()

                self.data.password_entry.unbind("<FocusOut>")
                self.data.confirm_pass_entry.unbind("<FocusOut>")

                self.data.password_entry.focus_out(callback=self.Callback_focusOut)
                self.data.confirm_pass_entry.focus_out(callback=self.Callback_focusOut)

                raise ValueError("password is not matching with confirm password")

            else:
                self.data.password_entry.configure(border_color=self.border_color)
                self.data.confirm_pass_entry.configure(border_color=self.border_color)

            if len(security_answer.strip(" ")) == 0:
                self.data.security_entry.unbind("<FocusIn>")
                self.data.security_entry.KeyChange()
                self.data.security_entry.focus()
                self.data.security_entry.configure(border_color=self.ERROR)
                raise ValueError("enter the secret answer.")

        except Exception as e:
            ...
            # CTkMessagebox(self, title="Error", message=f"{e}", icon="cancel")

        else:

            try:
                query = """
                    INSERT INTO teacher (
                    id, NAME, EMAIL, PASSWORD, GENDER, DEPARTMENT, SECRET_QUESTION, SECRET_ANSWER)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                t_id = sfg(node_id=1).generate_id()
                print(t_id)

                value = (t_id, name, email, confirm_password, gender, department,
                         security_question, security_answer)

                self.cursor = Execute(self.conn, query, value)

                # print("Teacher Data Inserted!")
                self.after(500, lambda: self.new_btn.configure(fg_color=self.SUCCESS))
                self.after(3000, lambda: self.new_btn.configure(fg_color="#3a7ebf"))

            except Exception as e:
                CTkMessagebox(self, title="Error", message=f"{e}", icon="cancel")

            else:
                # resetting all input
                self.data.name_entry.delete(0, ctk.END)
                self.data.email_entry.delete(0, ctk.END)
                self.data.password_entry.delete(0, ctk.END)
                self.data.confirm_pass_entry.delete(0, ctk.END)
                self.data.security_entry.delete(0, ctk.END)

                self.data.gender_combbx.current(0)
                self.data.dept_combbx.current(0)
                self.data.sec_comb.current(0)

    def Verify_password(self) -> bool:
        passw = self.data.password_entry.get().strip(" ")
        cpass = self.data.confirm_pass_entry.get().strip(" ")

        if len(passw) != 0 and len(cpass) != 0 and passw == cpass:
            return True
        return False


if __name__ == '__main__':
    app = ctk.CTk()
    Student_Register(app, 'Student')
    app.mainloop()
