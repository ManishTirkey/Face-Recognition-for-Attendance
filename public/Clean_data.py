import os

from DB import *
from DB_config import *
import shutil
from file_config import IMAGE_FOLDER


def Clean_DB():
    try:
        connection = ConnectDB()
        Execute(connection, Clean_data)
        print("Database is Cleaned")
    except Exception as e:
        print(e)
    else:
        Disconnect(connection)


# delete images and trained data

def delete_directory(directory):
    try:
        for sub_dir in os.listdir(directory):
            sub_path = os.path.join(directory, sub_dir)
            if os.path.isdir(sub_path):
                shutil.rmtree(sub_path)
        print(f"Directory '{directory}' successfully deleted.")
    except Exception as e:
        print(f"Error deleting directory '{directory}': {e}")


if __name__ == '__main__':
    Clean_DB()
    delete_directory(IMAGE_FOLDER)
