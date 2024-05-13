import os
import cv2
import pandas as pd
from threading import Thread

from src.components.DATETIME import Date as Today
from public.file_config import *
from public.DB import *

color_success = (34, 255, 105)
color_white = (255, 255, 255)
UIP_color = (255, 56, 82)


def Make_attendance(connection, s_id):
    query = """
    INSERT INTO attendance (
    student_id
    )
    VALUES (%s)
    """

    value = (s_id,)
    Execute(connection, query, value)


def Check_attendance(connection, s_id):
    query = """
    SELECT id FROM attendance WHERE student_id=%s AND created_at_date=%s
    """

    value = (s_id, Today())
    cursor = Execute_Fetch(connection, query, value)
    return cursor.fetchone()


def AllEmployeeDetection():
    connection = Connect()
    cam = None


    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINED_LABEL_IMAGE)

        facecasCade = cv2.CascadeClassifier(HAARCASCADE_FILE)
        cam = cv.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            frame, im = cam.read()
            im = cv2.flip(im, 1)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)

            if len(faces) > 0:

                for (x, y, w, h) in faces:
                    Id, confidence = recognizer.predict(gray[y: y + h, x: x + w])

                    if confidence < 70:

                        query = f"""
                        SELECT s.NAME
                        FROM face_mapping a
                        JOIN student s ON a.student_id = s.id
                        WHERE a.id=%s; 
                        """
                        value = (Id, )

                        cursor = Execute_Fetch(connection, query, value)

                        student = cursor.fetchone()
                        name = student[0]

                        tt = str(name).capitalize()

                        cv2.rectangle(im, (x, y), (x + w, y + h), color_success, 2)
                        cv2.putText(im, tt, (x, y-5), font, 1, color_white, 2)

                    else:
                        tt = "UIP"

                        cv2.rectangle(im, (x, y), (x + w, y + h), UIP_color, 2)
                        cv2.putText(im, tt, (x, y-5), font, 1, UIP_color, 2)

            cv2.imshow("Recognizing", im)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as e:
        raise e

    finally:
        if cam is not None:
            cam.release()
        cv2.destroyAllWindows()
        Disconnect(connection)


def Recognize():
    th = Thread(target=AllEmployeeDetection, daemon=False)
    th.start()


if __name__ == '__main__':
    Recognize()
