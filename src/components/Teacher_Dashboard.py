from public.DB import *
import customtkinter as ctk
from src.components.CustomCTKentry import Component_lb_en
from public.file_config import Security_questions, Departments, Semesters, Gender, Pre_Ab
from src.components.Register_style import Styling
import tkinter as tk
from tkinter import *
from tkinter import ttk
from random import choice


class Dashboard(ctk.CTkToplevel, Styling):
    # class Dashboard(ctk.CTk, Styling):
    def __init__(self, parent, t_id):
        ctk.CTkToplevel.__init__(self, master=parent)
        # ctk.CTk.__init__(self)
        Styling.__init__(self)
        self.t_id = t_id

        self.focus()

        self.con = Connect()
        self.cursor = None

        query = """
        SELECT NAME FROM teacher WHERE id=%s
        """
        value = (self.t_id,)
        self.cursor = Execute_Fetch(self.con, query, value)
        data = self.cursor.fetchone()

        name = data[0].capitalize()
        self.title(f"Teacher Dashboard: {name}")

        width = 1366
        height = 730

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position t751430
        # o center window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window position
        self.minsize(width, height)
        self.geometry(f"{width}x{height}+{x}+{y}")
        # self.attributes('-maximize', True)
        self.resizable(True, True)

        self.protocol("WM_DELETE_WINDOW", self.Destroy)

        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill=ctk.BOTH, expand=True, padx=2, pady=2)

        self.Information_build()
        self.Data()

    def Destroy(self):
        self.show_btn.unbind("<Enter>")
        self.reset_btn.unbind("<Enter>")
        self.roll_check_btn.unbind("<Enter>")

        self.show_btn.unbind("<Leave>")
        self.reset_btn.unbind("<Leave>")
        self.roll_check_btn.unbind("<Leave>")

        Disconnect(self.con)
        self.destroy()

    def Data(self):
        self.wrapper = Component_lb_en(self.main_container)
        self.wrapper.pack(side=ctk.RIGHT, fill=ctk.BOTH,
                          expand=True, padx=10, pady=10)
        self.wrapper.configure(border_width=1, border_color="#fff")

        self.display_container = Component_lb_en(self.wrapper)
        self.display_container.pack(fill='both', pady=20, padx=16)

        column = ('date', 'attendance_status', 'roll no', 'name', 'phone', "email", 'gender', 'dob', 'department', 'semester', 'admission date')

        scrool_x = ttk.Scrollbar(self.display_container, orient=HORIZONTAL)
        scrool_y = ttk.Scrollbar(self.display_container, orient=VERTICAL)
        scrool_x.pack(side=BOTTOM, fill=X)
        scrool_y.pack(side=RIGHT, fill=Y)

        self.display = ttk.Treeview(self.display_container,
                                    columns=column,
                                    show='headings',
                                    xscrollcommand=scrool_x.set,
                                    yscrollcommand=scrool_y.set
                                    )
        scrool_y.config(command=self.display.yview)
        scrool_x.config(command=self.display.xview)
        for i in column:
            self.display.heading(i, text=i.capitalize())

        self.display.pack(fill='both', expand=True, )
        for col in self.display['columns']:
            self.display.column(col, anchor="center", minwidth=100, width=120)

    def Insert_data_table(self, data):
        print(len(data))
        if len(data) == 0:
            return

        self.after(50, lambda: self.wrapper.configure(border_color=self.SUCCESS))
        self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))

        for item in self.display.get_children():
            self.display.delete(item)

        for row in data:
            self.display.insert(parent='', index='end', values=row)

    def Information_build(self):
        left_container = Component_lb_en(self.main_container)
        left_container.pack(side=ctk.LEFT, expand=False, padx=(1, 10), pady=10)

        left_wrapper = Component_lb_en(left_container)
        left_wrapper.pack(fill=ctk.BOTH, padx=10, pady=2)

        distance = (0, 20)

        heading_frame = Component_lb_en(left_wrapper)
        heading_frame.pack(pady=(0, 60))
        heading_frame.Label(text="Teacher Dashboard", anchor='w', font=("Ubuntu", 28, "bold"))

        department_frame = Component_lb_en(left_wrapper)
        department_frame.pack(padx=2, pady=distance)
        department_frame.Label(text="Department")
        self.department_combbx = department_frame.Combobox(combobox_values=Departments)

        semester_frame = Component_lb_en(left_wrapper)
        semester_frame.pack(padx=2, pady=distance)
        semester_frame.Label(text="Semester")
        self.semester_combbx = semester_frame.Combobox(combobox_values=Semesters)

        ab_pre_frame = Component_lb_en(left_wrapper)
        ab_pre_frame.pack(padx=2, pady=distance)
        ab_pre_frame.Label(text="Present/Absent")
        self.ab_pre_combbx = ab_pre_frame.Combobox(combobox_values=Pre_Ab)

        btns = Component_lb_en(left_wrapper)
        btns.pack(pady=(20, 0))
        self.show_btn = btns.Button(text="show", text_color=self.SAVE_BTN, font=("", 16,))
        self.show_btn.configure(fg_color=self.bg_color, hover=False, border_width=1,
                                border_color=self.SAVE_DULL_BTN,
                                command=self.Show)
        self.show_btn.pack(side=ctk.LEFT, padx=30)
        self.show_btn.bind("<Enter>", lambda e: self.Enter(self.show_btn, self.SAVE_BTN))
        self.show_btn.bind("<Leave>", lambda e: self.Leave(self.show_btn, self.SAVE_DULL_BTN))

        self.reset_btn = btns.Button(text="Reset", text_color=self.RESET_BTN, font=("", 16,))
        self.reset_btn.configure(fg_color=self.bg_color, hover=False, border_width=1,
                                 border_color=self.RESET_DULL_BTN, command=self.Reset)
        self.reset_btn.pack(side=ctk.RIGHT, padx=30)
        self.reset_btn.bind("<Enter>", lambda e: self.Enter(self.reset_btn, self.RESET_BTN))
        self.reset_btn.bind("<Leave>", lambda e: self.Leave(self.reset_btn, self.RESET_DULL_BTN))

        roll_frame = Component_lb_en(left_wrapper)
        roll_frame.pack(pady=(30, 0))
        roll_frame.Label(text="Roll No.")
        self.roll_entry = roll_frame.Entry(placeholder_text="Enter Roll no....")
        self.roll_check_btn = roll_frame.Button(text="Check", text_color=self.SAVE_BTN, font=("", 16,),
                                                command=self.Roll_Check)
        self.roll_check_btn.pack(pady=(10, 0), padx=4)
        self.roll_check_btn.configure(hover=False, border_width=1, fg_color=self.bg_color,
                                      border_color=self.SAVE_DULL_BTN)
        self.roll_check_btn.bind("<Enter>", lambda e: self.Enter(self.roll_check_btn, self.SAVE_BTN))
        self.roll_check_btn.bind("<Leave>", lambda e: self.Leave(self.roll_check_btn, self.SAVE_DULL_BTN))

    @staticmethod
    def Enter(button, color):
        button.configure(border_color=color)

    #
    @staticmethod
    def Leave(button, color):
        button.configure(border_color=color)

    def Show(self):
        department = self.department_combbx.get()
        semester = self.semester_combbx.get()
        attendance = self.ab_pre_combbx.get()

        if department.lower() == "select" or semester.lower() == "select":
            print("not selected")
            self.after(500, lambda: self.wrapper.configure(border_color=self.ERROR))
            self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))
            return

        if attendance.lower() is "absent":
            # absent query
            query = """
            SELECT attendance.created_at_date, ROLL, NAME, PHONE, EMAIL, GENDER, DOB, DEPARTMENT, SEMESTER, student.created_at_date
            FROM student LEFT OUTER JOIN attendance ON student.id=attendance.student_id 
            WHERE attendance.id IS NULL and DEPARTMENT=%s and SEMESTER=%s;
            """
        else:
            # present query
            query = """select attendance.created_at_date, ROLL, NAME, PHONE, EMAIL, GENDER, DOB, DEPARTMENT, SEMESTER, student.created_at_date             
            from student left outer join attendance on student.id=attendance.student_id 
            where attendance.id is not NULL and DEPARTMENT=%s and SEMESTER=%s;
            """
        values = (department, semester)

        self.cursor = Execute_Fetch(self.con, query, values)
        rows = self.cursor.fetchall()
        print(rows)

        self.Insert_data_table(rows)

    def Reset(self):
        self.after(500, lambda: self.wrapper.configure(border_color=self.SUCCESS))
        self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))
        self.department_combbx.current(0)
        self.semester_combbx.current(0)
        self.ab_pre_combbx.current(0)

    def Roll_Check(self):
        roll = self.roll_entry.get().strip(" ")

        if not roll.isnumeric() or len(roll) == 0:
            self.after(500, lambda: self.wrapper.configure(border_color=self.ERROR))
            self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))
            return

        roll = int(roll)
        # query = """
        # SELECT ROLL, NAME, PHONE, EMAIL, GENDER, DOB, DEPARTMENT, SEMESTER, created_at_date
        # FROM student WHERE ROLL=%s
        # """
        query = """
        SELECT attendance.created_at_date,  
        
        CASE
        WHEN attendance.student_id IS NULL THEN 'Absent'
        ELSE 'Present'
        END AS Attendance_Status,
        
        ROLL, NAME, PHONE, EMAIL, GENDER, DOB, DEPARTMENT, SEMESTER, student.created_at_date
        
        FROM student 
        LEFT OUTER JOIN attendance ON student.id=attendance.student_id WHERE student.roll=%s;
        """
        value = (roll,)
        self.cursor = Execute_Fetch(self.con, query, value)
        data = self.cursor.fetchone()

        if data is None or len(data) == 0:
            self.after(500, lambda: self.wrapper.configure(border_color=self.ERROR))
            self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))
            return

        self.Insert_data_table([data])


if __name__ == '__main__':
    app = ctk.CTk()
    Dashboard(app, "1io2qspjj7k00")
    app.mainloop()
