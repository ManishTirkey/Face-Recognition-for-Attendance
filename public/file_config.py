from typing import List
from pathlib import Path
import cv2 as cv
import os


# * -----------------------------

# * base dir of project

BASE_DIR = Path(__file__).resolve().parent.parent

# * public files
Component_img = os.path.join(BASE_DIR, "public/component_img")
HAARCASCADE_FILE = os.path.join(BASE_DIR, "public/haarcascade_frontalface_default.xml")
TRAINED_LABEL_IMAGE = os.path.join(BASE_DIR, "public/TrainedData/Trainner.yaml")
IMAGE_FOLDER = os.path.join(BASE_DIR, "public/Images")

# * configuration
Pre_Ab: List[str] = ["Present", "Absent"]
Gender: List[str] = ["Select", "Male", "Female", "Others"]
Security_questions: List[str] = ["Your Birth Place ?", "Your Pet Name ?", "Your Birth Year ?"]

# * Student configuration
Departments: List[str] = ["Select", "MCA", "MS.c IT"]
Semesters: List[str] = ["Select", "Sem I", "Sem II", "Sem III", "Sem IV", ]

