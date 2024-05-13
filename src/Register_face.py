import os
import cv2

from public.file_config import *
from src.Detect_face import Detect_Face
from src.Train_data import TrainImage
from public.DB import *


msg = "Not allowed multiple faces"
font = cv2.FONT_HERSHEY_SIMPLEX
msg_color = (255, 255, 255)
font_scale = .6
font_thickness = 2


def Take_image(img_dir: str = None, faceID: int = None, callback=None):
    connection = Connect()

    img_dir = os.path.join(img_dir, str(faceID))

    if not os.path.exists(img_dir):
        Path(img_dir).mkdir(parents=True, exist_ok=True)
    else:
        img_dir = None

    cam = cv.VideoCapture(0)
    sampleNum = 1

    try:
        while True:
            ret, img = cam.read()
            img, detect, faces = Detect_Face(img, color=(123, 234, 34))
            img_height, img_width = img.shape[:2]

            # if len(faces) > 0 and detect:
            #     for (w, h) in faces:
            #         cv2.rectangle(img, w, h, (0, 0, 0), 2)

            if len(faces) > 1:
                # raise error not allowed multiple face at a time

                cv2.putText(img,
                            msg, (10, img_height - 10),
                            fontFace=font, fontScale=font_scale,
                            color=msg_color, thickness=font_thickness)

            if len(faces) == 1 and img_dir is not None:
                # make face register

                img_path = os.path.join(img_dir, f"{faceID}_{str(sampleNum)}.jpg")

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                cv2.putText(img, f"Quit: q, Sample: {sampleNum}",
                            (10, img_height - 10),
                            fontFace=font, fontScale=font_scale,
                            color=msg_color, thickness=font_thickness)

                for (w, h) in faces:
                    # p = x + w
                    # q = y + h
                    x, y = w
                    p, q = h
                    cv2.imwrite(img_path, gray[y: q, x: p])

                sampleNum = sampleNum + 1

            cv2.imshow(f"{faceID}", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as e:
        ...

    else:
        try:
            callback(faceID)
        except Exception as e:
            import shutil
            shutil.rmtree(img_dir)
            return

    cam.release()
    cv2.destroyAllWindows()

    query = """
    INSERT INTO face_mapping (
    student_id
    )
    VALUES(%s)                
    """

    value = (faceID, )
    Execute(connection, query, value)

    TrainImage()


if __name__ == '__main__':
    # Testing
    Take_image(IMAGE_FOLDER, 12)
