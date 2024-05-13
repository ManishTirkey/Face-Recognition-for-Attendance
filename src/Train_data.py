import os
import cv2
import os

import numpy as np
from PIL import Image
from threading import Thread
from pathlib import Path
from CTkMessagebox import CTkMessagebox

from public.file_config import IMAGE_FOLDER, TRAINED_LABEL_IMAGE
from public.DB import *


def Train_Image(connection):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id = getImagesAndLabel(connection)
    recognizer.train(faces, np.array(Id))
    recognizer.save(TRAINED_LABEL_IMAGE)

    CTkMessagebox(title="Image Training", message=f"Image Training Successfully", icon="check", option_1="Done")


def getImagesAndLabel(connection, path=IMAGE_FOLDER):
    new_dir = np.array([], dtype=object)
    for dire in os.listdir(path):
        di = np.array([os.path.join(path, dire)], dtype=object)
        new_dir = np.concatenate([new_dir, di])

    imagePath = np.array([], dtype=object)
    for i in new_dir:
        for file in os.listdir(i):
            img_file = np.array([os.path.join(i, file)], dtype=object)
            imagePath = np.concatenate([imagePath, img_file])

    faces = []
    Ids = []

    for i_path in imagePath:
        pilImage = Image.open(i_path).convert("L")
        imageNp = np.array(pilImage, "uint8")

        Id = Path(i_path).stem.split("_")[0]

        query = f"""SELECT id FROM face_mapping WHERE student_id="{Id}";"""
        cursor = Execute_Fetch(connection, query)
        face_id = cursor.fetchone()[0]

        faces.append(imageNp)
        Ids.append(face_id)
    return faces, Ids


def TrainImage():
    connection = Connect()
    th = Thread(target=Train_Image, daemon=False, args=(connection, ))
    th.start()
    th.join()
    Disconnect(connection)


if __name__ == '__main__':
    # Train_Image()
    TrainImage()

