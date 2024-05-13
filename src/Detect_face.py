import os
import cv2
from public.file_config import *


def Detect_Face(img, flip=None, color=None):
    detect = 0
    face = []

    detector = cv2.CascadeClassifier(HAARCASCADE_FILE)

    if flip is not None:
        img = cv2.flip(img, flip)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        detect = 1

        for (x, y, w, h) in faces:
            p = x + w
            q = y + h

            face.append([(x, y), (p, q)])

            if color is not None:
                cv2.rectangle(img, (x, y), (p, q), color, 2)

    return [img, detect, face]

