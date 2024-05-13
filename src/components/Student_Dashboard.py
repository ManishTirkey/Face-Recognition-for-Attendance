from public.DB import *
import customtkinter as ctk
from src.components.CustomCTKentry import Component_lb_en
from public.file_config import Security_questions, Departments, Semesters, Gender
from src.components.Register_style import Styling
from tkinter import ttk
from tkinter import *
from src.components.DATETIME import Current_month_date_list


class Dashboard(ctk.CTkToplevel, Styling):
    # class Dashboard(ctk.CTk, Styling):
    def __init__(self, parent, s_id):
        ctk.CTkToplevel.__init__(self, master=parent)
        # ctk.CTk.__init__(self)
        Styling.__init__(self)
        self.s_id = s_id

        self.con = Connect()
        self.cursor = None

        query = """
        SELECT NAME FROM student WHERE id=%s
        """
        value = (self.s_id,)
        self.cursor = Execute_Fetch(self.con, query, value)
        data = self.cursor.fetchone()

        name = data[0].capitalize()
        self.title(f"Student Dashboard: {name}")

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
        # self.main_container.configure(border_width=1,
        #                               border_color="#fff")

        self.Get_student_info()
        self.Information_build()
        self.Data()
        self.Insert_Data()

    def Destroy(self):
        self.save_btn.unbind("<Enter>")
        self.reset_btn.unbind("<Enter>")

        self.save_btn.unbind("<Leave>")
        self.reset_btn.unbind("<Leave>")

        Disconnect(self.con)
        self.destroy()

    def Data(self):
        self.wrapper = Component_lb_en(self.main_container)
        self.wrapper.pack(side=ctk.RIGHT, fill=ctk.BOTH,
                     expand=True, padx=10, pady=10)
        self.wrapper.configure(border_width=1, border_color="#fff")

        self.display_container = Component_lb_en(self.wrapper)
        self.display_container.pack(fill='both', pady=20, padx=16)

        column = ('date', 'attendance_status')

        scrool_x = ttk.Scrollbar(self.display_container, orient=HORIZONTAL)
        scrool_y = ttk.Scrollbar(self.display_container, orient=VERTICAL)
        scrool_x.pack(side=BOTTOM, fill=X)
        scrool_y.pack(side=RIGHT, fill=Y)

        self.display = ttk.Treeview(self.display_container, columns=column, selectmode='browse',
                                    show='headings',
                                    xscrollcommand=scrool_x.set,
                                    yscrollcommand=scrool_y.set
                                    )
        scrool_y.config(command=self.display.yview)
        scrool_x.config(command=self.display.xview)
        for i in column:
            self.display.heading(i, text=i.capitalize())

        self.display.pack(fill='both', expand=True)
        for col in self.display['columns']:
            self.display.column(col, anchor="center", minwidth=100, width=120)

    def Insert_Data(self):
        for date in Current_month_date_list():
            self.Search_data(date)

    def Search_data(self, date):
        attendance_status = 'Present'
        query = """
        SELECT id FROM attendance WHERE student_id=%s AND created_at_date=%s;
        """
        values = (self.s_id, date)
        self.cursor = Execute_Fetch(self.con, query, values)

        row = self.cursor.fetchone()

        if row is None or len(row) == 0:
            attendance_status = 'Absent'

        data = (date, attendance_status)
        self.display.insert(parent='', index='end', values=data)

    def Information_build(self):
        left_container = Component_lb_en(self.main_container)
        left_container.pack(side=ctk.LEFT, expand=False, padx=(1, 10), pady=10)

        left_wrapper = Component_lb_en(left_container)
        left_wrapper.pack(fill=ctk.BOTH, padx=10, pady=2)

        distance = (0, 4)

        heading = left_wrapper.Label(text="Student Details",
                                     anchor='w',
                                     font=("Ubuntu", 28, "bold"))
        heading.pack(pady=(0, 20))

        admission_details = Component_lb_en(left_wrapper)
        admission_details.pack(pady=distance)

        roll_frame = Component_lb_en(admission_details)
        roll_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, pady=0, padx=4)
        roll_label = roll_frame.Label(text="Roll No.")
        self.roll_entry = roll_frame.Entry()
        self.roll_entry.insert(0, self.roll)
        self.roll_entry.configure(state="disabled")

        admission_date_frame = Component_lb_en(admission_details)
        admission_date_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, pady=0, padx=4)
        admission_date_frame.Label(text="Admission Date")
        self.admission_date_entry = admission_date_frame.Entry()
        self.admission_date_entry.insert(0, self.admission_date)
        self.admission_date_entry.configure(state="disabled")

        name_frame = Component_lb_en(left_wrapper)
        name_frame.pack(pady=distance)
        name_frame.Label(text="Name")
        self.name_entry = name_frame.Entry(placeholder_text="Enter name...")
        self.name_entry.insert(0, self.name)

        gender_dob_container = Component_lb_en(left_wrapper)
        gender_dob_container.pack(pady=distance)

        gender_frame = Component_lb_en(gender_dob_container)
        gender_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=4, pady=0)
        gender_frame.Label(text="Gender")
        self.gender_combbx = gender_frame.Combobox(combobox_values=Gender)
        self.gender_combbx.current(self.gender_index)

        dob_frame = Component_lb_en(gender_dob_container)
        dob_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=4, pady=0)
        dob_frame.Label(text="DOB")
        dob = dob_frame.Entry()
        dob.insert(0, "dob")
        dob.configure(state="disabled")

        email_frame = Component_lb_en(left_wrapper)
        email_frame.pack(pady=distance)
        email_frame.Label(text="Email")
        self.email_entry = email_frame.Entry(placeholder_text="Email...")
        self.email_entry.insert(0, self.email)

        phone_frame = Component_lb_en(left_wrapper)
        phone_frame.pack(pady=distance)
        phone_frame.Label(text="Phone")
        self.phone_entry = phone_frame.Entry(placeholder_text="Phone no...")
        self.phone_entry.insert(0, self.phone)

        depart_sem_container = Component_lb_en(left_wrapper)
        depart_sem_container.pack(pady=distance)

        department_frame = Component_lb_en(depart_sem_container)
        department_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=4, pady=distance)
        department_frame.Label(text="Department")
        self.department_combbx = department_frame.Combobox(combobox_values=Departments)
        self.department_combbx.current(self.department_index)
        self.department_combbx.configure(state="disabled")

        semester_frame = Component_lb_en(depart_sem_container)
        semester_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=4, pady=distance)
        semester_frame.Label(text="Semester")
        self.semester_combbx = semester_frame.Combobox(combobox_values=Semesters)
        self.semester_combbx.current(self.semester_index)
        self.semester_combbx.configure(state="disabled")

        secret_frame = Component_lb_en(left_wrapper)
        secret_frame.pack(pady=distance)
        secret_frame.Label(text="Secret Question")
        self.secret_combbx = secret_frame.Combobox(combobox_values=Security_questions)
        self.secret_combbx.current(self.secret_q_index)

        self.secret_a_entry = secret_frame.Entry(placeholder_text="Secret answer...")
        self.secret_a_entry.pack(pady=(2, 0))
        self.secret_a_entry.insert(0, self.secret_a)

        btns = Component_lb_en(left_wrapper)
        btns.pack(pady=(20, 0))
        self.save_btn = btns.Button(text="Save", text_color=self.SAVE_BTN,
                                    font=("", 16,))
        self.save_btn.configure(fg_color=self.bg_color, hover=False, border_width=1,
                                border_color=self.SAVE_DULL_BTN, command=self.Update)
        self.save_btn.pack(side=ctk.LEFT, padx=30)
        self.save_btn.bind("<Enter>", lambda e: self.Enter(self.save_btn, self.SAVE_BTN))
        self.save_btn.bind("<Leave>", lambda e: self.Leave(self.save_btn, self.SAVE_DULL_BTN))

        self.reset_btn = btns.Button(text="Reset", text_color=self.RESET_BTN, font=("", 16,))
        self.reset_btn.configure(fg_color=self.bg_color, hover=False, border_width=1,
                                 border_color=self.RESET_DULL_BTN, command=self.Reset)
        self.reset_btn.pack(side=ctk.RIGHT, padx=30)
        self.reset_btn.bind("<Enter>", lambda e: self.Enter(self.reset_btn, self.RESET_BTN))
        self.reset_btn.bind("<Leave>", lambda e: self.Leave(self.reset_btn, self.RESET_DULL_BTN))

    @staticmethod
    def Enter(button, color):
        button.configure(border_color=color)

    #
    @staticmethod
    def Leave(button, color):
        button.configure(border_color=color)

    def Get_student_info(self):
        query = f"""
        SELECT 
        ROLL, EMAIL, NAME, PHONE, DEPARTMENT, SEMESTER,
        DOB, GENDER, SECRET_QUESTION, SECRET_ANSWER, created_at_date
        FROM student WHERE id=%s 
        """
        value = (self.s_id,)
        self.cursor = Execute_Fetch(self.con, query, value)

        self.data = self.cursor.fetchone()

        self.roll = self.data[0]
        self.email = self.data[1]
        self.name = self.data[2]
        self.phone = self.data[3]
        department = self.data[4]
        semester = self.data[5]
        self.dob = self.data[6]
        gender = self.data[7]
        secret_q = self.data[8]
        self.secret_a = self.data[9]
        self.admission_date = self.data[10]

        self.gender_index = Gender.index(gender)
        self.department_index = Departments.index(department)
        self.semester_index = Semesters.index(semester)
        self.secret_q_index = Security_questions.index(secret_q)

    def Update(self):
        name = self.name_entry.get()
        gender = self.gender_combbx.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        secret_q = self.secret_combbx.get()
        secret_a = self.secret_a_entry.get()

        query = """ 
        UPDATE student SET 
        EMAIL=%s, NAME=%s, PHONE=%s, GENDER=%s, SECRET_QUESTION=%s, SECRET_ANSWER=%s
        WHERE id=%s
        """
        values = (email, name, phone, gender, secret_q, secret_a, self.s_id)
        try:
            Execute(self.con, query, values)
        except Exception as e:
            self.after(500, lambda: self.wrapper.configure(border_color=self.ERROR))
            self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))
        else:
            self.after(500, lambda: self.wrapper.configure(border_color=self.SUCCESS))
            self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))

    def Reset(self):
        self.after(500, lambda: self.wrapper.configure(border_color=self.SUCCESS))
        self.after(2000, lambda: self.wrapper.configure(border_color="#fff"))

        self.name_entry.delete(0, ctk.END)
        self.name_entry.configure(placeholder_text="Enter name...")

        self.gender_combbx.current(0)

        self.email_entry.delete(0, ctk.END)
        self.email_entry.configure(placeholder_text="Email...")

        self.phone_entry.delete(0, ctk.END)
        self.phone_entry.configure(placeholder_text="Phone no....")

        self.secret_combbx.current(0)
        self.secret_a_entry.delete(0, ctk.END)
        self.secret_a_entry.configure(placeholder_text="Secret answer....")


if __name__ == '__main__':
    app = ctk.CTk()
    dash = Dashboard(app, "1inpkz0akei9s")
    app.mainloop()
