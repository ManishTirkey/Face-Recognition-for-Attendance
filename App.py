from tkinter import *

import customtkinter as ctk
from customtkinter import CTk
from ctypes import windll, c_int, byref, sizeof

from PIL import ImageTk, Image
import os

from src.components.DATETIME import Date, Time
from src.components.forget_password import forget_password
from src.components.Register import Student_Register, Teacher_Register
from src.components.Login import Login
from public.file_config import Component_img
from src.Recognize import Recognize

ctk.set_appearance_mode("dark")


# ctk.ThemeManager.load_theme("green")

# *-------------------Functions

# def ModeStr() -> str:
#     if ctk.get_appearance_mode() == "Light":
#         return "Switch to Dark"
#     return "Switch to Light"


def ToggleAppearance_mode() -> None:
    if ctk.get_appearance_mode() == "Light":
        ctk.set_appearance_mode('dark')
        # theme_mode.configure(text="Switch to Light")
    else:
        ctk.set_appearance_mode('light')
        # theme_mode.configure(text="Switch to Dark")


# *-------------------End-Function

width = 1200
height = 600

app = CTk()
app.title("Dashboard")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate position to center window
x = (screen_width - width) // 2
y = (screen_height - height) // 2

# Set window position
app.geometry(f"{width}x{height}+{x}+{y}")

app.resizable(False, False)
app.update_idletasks()

# *----------------------Variables

# Appearance_mode = ctk.StringVar(value="dark")

# ------sideBar

sideBar_light = "#ECF0F1"
sideBar_dark = "#464646"
sidebar_label_anchor = E

right = 20
sidebar_label_padx = (20, right)
sidebar_label_font = ("Ubuntu", 18, "bold")
img_position = 'right'
tea_stu_distance = (30, 15)
btn_paddingx = (0, right)
btn_paddingy = (8, 0)
size = (25, 25)

wrapper_color = ("#e6e6e6", "#2A2A2A")
wrapper_bd_color = ("#e6e6e6", "#1b1b1b")
atten_btn_color = ("#E74C3C", "#9B59B6")
atten_btn_hover = ("#D5D5D5", "#181818")
atten_btn_font = ("ubuntu", 24, "bold")

# *----------------------End-Variables

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill=BOTH, expand=True)

container = ctk.CTkFrame(main_frame)
container.pack(side=TOP, fill=BOTH, expand=True)

status_frame = ctk.CTkFrame(main_frame,
                            fg_color=("#E5E8E8", "#515A5A"))
status_frame.pack(side=BOTTOM, fill=X)

time_status = ctk.CTkLabel(status_frame,
                           text=f"{Time()}",
                           font=("Tahoma", 16, "bold"),
                           text_color=('#566573', '#D7DBDD'))
time_status.pack(side=RIGHT)
time_status.configure(padx=20, pady=10)

divider = ctk.CTkFrame(status_frame,
                       width=2,
                       height=25,
                       fg_color=("#ABB2B9", "#BDC3C7"))
divider.pack(side=RIGHT)

date_status = ctk.CTkLabel(status_frame,
                           text=f"{Date()}",
                           font=("Tahoma", 16, "bold"),
                           text_color=('#566573', '#D7DBDD'))
date_status.pack(side=RIGHT)
date_status.configure(padx=20, pady=10)

copyright = ctk.CTkLabel(status_frame,
                         text="Copyright@ 2024,",
                         font=("Segoe Script", 12, "bold"),
                         text_color="#fff"
                         )
copyright.pack(side=LEFT, padx=(40, 4))

sign = ctk.CTkLabel(status_frame,
                    text="ManishTirkey",
                    font=("Jua", 18, "normal"),
                    text_color="#fff"
                    )
sign.pack(side=LEFT, padx=(4, 10))

# *----------------------------side bar content

sideBar = ctk.CTkFrame(container)
sideBar.pack(side=RIGHT, fill=Y, ipadx=50)

Theme_container = ctk.CTkFrame(sideBar,
                               height=100,
                               corner_radius=0,
                               fg_color=(sideBar_light, sideBar_dark)
                               )
Theme_container.pack(side=TOP, fill=X)

theme_mode = ctk.CTkSwitch(Theme_container,
                           text="  Theme",
                           command=ToggleAppearance_mode,

                           progress_color="#283747",
                           button_color="#1ABC9C",
                           fg_color="#F2F3F4",
                           button_hover_color="#EC7063",
                           )
theme_mode.pack(side=LEFT, padx=(30, 0), pady=(20, 30))

sideBar_content_container = ctk.CTkFrame(sideBar,
                                         corner_radius=0,
                                         fg_color=(sideBar_light, sideBar_dark))
sideBar_content_container.pack(side=BOTTOM, fill=BOTH, expand=True)

# ----------------Teacher

teacher = ctk.CTkFrame(sideBar_content_container,
                       corner_radius=0,
                       fg_color=(sideBar_light, sideBar_dark))
teacher.pack(side=BOTTOM, fill=X, pady=tea_stu_distance)

teacher_label = ctk.CTkLabel(teacher,
                             text="Teacher",
                             anchor=sidebar_label_anchor,
                             font=sidebar_label_font
                             )
teacher_label.pack(fill=X, padx=sidebar_label_padx)

login_tea_img = Image.open(os.path.join(Component_img, "login_512.png"))
login_tea_ctk = ctk.CTkImage(login_tea_img, size=size)

tea_login = ctk.CTkFrame(teacher,
                         corner_radius=0,
                         fg_color=(sideBar_light, sideBar_dark)
                         )
tea_login.pack(fill=X)

tea_login_btn = ctk.CTkButton(tea_login,
                              text="Teacher Login",
                              image=login_tea_ctk,
                              compound=img_position,
                              command=lambda: Login(app, title="teacher")
                              )
tea_login_btn.pack(side=RIGHT, padx=btn_paddingx, pady=btn_paddingy)

reg_tea_img = Image.open(os.path.join(Component_img, "reg_512.png"))
reg_tea_ctk = ctk.CTkImage(reg_tea_img, size=size)

tea_reg = ctk.CTkFrame(teacher,
                       corner_radius=0,
                       fg_color=(sideBar_light, sideBar_dark)
                       )
tea_reg.pack(fill=X)

tea_reg_btn = ctk.CTkButton(tea_reg,
                            text="New Teacher Register",
                            command=lambda: Teacher_Register(app),
                            image=reg_tea_ctk,
                            compound=img_position)
tea_reg_btn.pack(side=RIGHT, pady=btn_paddingy, padx=btn_paddingx)

fp_tea_img = Image.open(os.path.join(Component_img, "forgot-password.png"))
fp_tea_ctk = ctk.CTkImage(fp_tea_img, size=size)

tea_fp = ctk.CTkFrame(teacher,
                      corner_radius=0,
                      fg_color=(sideBar_light, sideBar_dark)
                      )
tea_fp.pack(fill=X)

tea_fp_btn = ctk.CTkButton(tea_fp,
                           text="Forget Password",
                           command=lambda: forget_password(app, "teacher"),
                           image=fp_tea_ctk,
                           compound=img_position)
tea_fp_btn.pack(side=RIGHT, pady=btn_paddingy, padx=btn_paddingx)
# -----------------------

divider1 = ctk.CTkFrame(sideBar_content_container,
                        height=2,
                        fg_color=("#D5D8DC", "#515A5A"))
divider1.pack(side=BOTTOM, fill=X, padx=(40, right), pady=(40, 0))

# --------------------student

student = ctk.CTkFrame(sideBar_content_container,
                       corner_radius=0,
                       fg_color=(sideBar_light, sideBar_dark))
student.pack(side=BOTTOM, fill=X)

stu_label = ctk.CTkLabel(student,
                         text="Student",
                         anchor=sidebar_label_anchor,
                         font=sidebar_label_font
                         )
stu_label.pack(fill=X, padx=sidebar_label_padx)

login_stu_img = Image.open(os.path.join(Component_img, "login_512.png"))
login_stu_ctk = ctk.CTkImage(login_stu_img, size=size)

stu_login = ctk.CTkFrame(student,
                         corner_radius=0,
                         fg_color=(sideBar_light, sideBar_dark)
                         )
stu_login.pack(fill=X)

stu_login_btn = ctk.CTkButton(stu_login,
                              text="Student Login",
                              image=login_stu_ctk,
                              compound=img_position,
                              command=lambda: Login(app, title="student")
                              )
stu_login_btn.pack(side=RIGHT, padx=btn_paddingx, pady=btn_paddingy)

reg_stu_img = Image.open(os.path.join(Component_img, "reg_512.png"))
reg_stu_ctk = ctk.CTkImage(reg_stu_img, size=size)

stu_reg = ctk.CTkFrame(student,
                       corner_radius=0,
                       fg_color=(sideBar_light, sideBar_dark)
                       )
stu_reg.pack(fill=X)

stu_reg_btn = ctk.CTkButton(stu_reg,
                            text="New Student Register",
                            command=lambda: Student_Register(app),
                            image=reg_stu_ctk,
                            compound=img_position)
stu_reg_btn.pack(side=RIGHT, pady=btn_paddingy, padx=btn_paddingx)

stu_fp = ctk.CTkFrame(student,
                      corner_radius=0,
                      fg_color=(sideBar_light, sideBar_dark)
                      )
stu_fp.pack(fill=X)

fp_stu_img = Image.open(os.path.join(Component_img, "forgot-password.png"))
fp_stu_ctk = ctk.CTkImage(fp_stu_img, size=size)

stu_fp_btn = ctk.CTkButton(stu_fp,
                           text="Forget Password",
                           command=lambda: forget_password(app, "student"),
                           image=fp_stu_ctk,
                           compound=img_position)
stu_fp_btn.pack(side=RIGHT, pady=btn_paddingy, padx=btn_paddingx)

# *----------------------------side bar content


# *-----------------------------main
wrapper = ctk.CTkFrame(container,
                       border_width=2,
                       border_color=wrapper_bd_color,
                       corner_radius=4,
                       fg_color=wrapper_color
                       )
wrapper.pack(side=LEFT,
             fill=BOTH,
             expand=True,
             padx=40,
             pady=(40, 40)
             )

title = ctk.CTkLabel(wrapper,
                     text="Facial Recognization System....",
                     font=("Ubuntu", 18, "bold")
                     )
title.pack(fill=X, pady=(20, 10), padx=10)

attendance_btn = ctk.CTkButton(wrapper,
                               text="Take Attendance",
                               border_width=4,
                               border_color=atten_btn_color,
                               text_color=atten_btn_color,
                               fg_color=wrapper_color,
                               hover_color=atten_btn_hover,
                               corner_radius=4,
                               font=atten_btn_font,
                               command=Recognize
                               )
attendance_btn.pack(side=BOTTOM, pady=(10, 30), ipadx=25, ipady=5)

main_img = ctk.CTkImage(Image.open(os.path.join(Component_img, 'bg-2.jpg')),
                        size=(400, 280))
image = ctk.CTkLabel(wrapper, image=main_img, text="")
image.pack(side=BOTTOM, fill=X, padx=20)


def Reset_time():
    time_status.configure(text=f"{Time()}")
    time_status.after(1000, Reset_time)


Reset_time()


def Destroy():
    app.unbind("<Return>")
    app.destroy()


app.protocol("WM_DELETE_WINDOW", Destroy)
app.bind("<Return>", lambda e: Recognize())

app.mainloop()
