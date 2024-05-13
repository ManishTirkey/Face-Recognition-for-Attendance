from DB import *
from DB_config import Create_DB
from datetime import datetime
# ----------------------- creating DB and tables


def CreateDB():
    try:
        Conn = ConnectDB()
        cur = Execute(Conn, Create_DB)

    except mysql.connector.Error as err:
        print(err)

    else:
        Disconnect(Conn, cur)
        print("Database Created")


def InitializeAllTables(q):
    try:
        Conn = Connect()
        cur = Execute(Conn, q)

    except mysql.connector.Error as err:
        print(err)

    else:
        Disconnect(Conn, cur)
        print(f"Query: {q}")
        print("------------------------Done")


# def InsertData():
#     conn = Connect()
#
#     # query = """
#     #
#     # INSERT INTO student (
#     #     student_id, ROLL, EMAIL, PHONE, DEPT, SEM, BIRTH, GEN,
#     #     PASS, SEQQ, SEQA
#     # )
#     #
#     # VALUES ('123456799', 'S01', 'johnaa.doe@example.com',
#     #         '1234567890', 'Computer Science', '4',
#     #         '2000-01-01', 'Male', 'password123',
#     #         'question1', 'answer1')
#     # """
#
#     # query = """
#     # INSERT INTO teacher (
#     # NAME, EMAIL, PASSWORD, GENDER, DEPARTMENT, SECRET_QUESTION, SECRET_ANSWER)
#     # VALUES (%s, %s, %s, %s, %s, %s, %s)
#     # """
#     #
#     # value = ('Manish', 'johnaaa.doe@example.com',
#     #          'admin', 'male', 'Computer', 'question1', 'answer1')
#
#     # query = """
#     # INSERT INTO student (
#     # id, ROLL, EMAIL, NAME, PHONE, DEPARTMENT, SEMESTER, GENDER,
#     # PASSWORD, SECRET_QUESTION, SECRET_ANSWER
#     # )
#     # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     # """
#     #
#     # value = ("12", "12", "sljdgsdfsdffdd", "manisha", "384579834", "jskd", "2", "male",
#     #          "pass", "secQ", "secA")
#     # Execute(conn, query, value)
#
#     # -----------------------
#
#     # query = "select * from teacher WHERE EMAIL=%s"
#     # value = ("indrani@gmail.com")
#     #
#     # cursor = Execute_Fetch(conn, query, value)
#     #
#     # # print(cursor.fetchall())  # return list
#     # print(cursor.fetchone())  # return
#     # # print(cursor.fetchmany())  # return list
#     # Disconnect(conn)
#
#     # ----------------------------
#     # table_name = "student"
#     # confirm = "manisha"
#     # email = "indrani@gmail.com"
#     #
#     # # "UPDATE `registration` SET `email` = 'admin@gmail.com' WHERE `registration`.`id` = 4;"
#     # query = f"""
#     #             UPDATE {table_name} SET PASSWORD = "{confirm}" WHERE EMAIL = "{email}";
#     #             """
#     # # value = (table_name, confirm, email)
#     #
#     # Execute(conn, query)
#
#     # ----------------------------
#
#     query = """
#         INSERT INTO face_mapping (
#         student_id
#         )
#         VALUES (%s)
#         """
#
#     value = ("12",)
#     Execute(conn, query, value)
#
#     Disconnect(conn)


def InitializeDB():
    CreateDB()
    # InitializeAllTables(Student_table)
    # InitializeAllTables(Teacher_table)
    # InitializeAllTables(Attendance_table)

    for table in CREATE_TABLE:
        InitializeAllTables(table)


if __name__ == "__main__":
    InitializeDB()

    # InsertData()




