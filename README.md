![Light Mode](https://github.com/ManishTirkey/Face-Recognition-for-Attendance-/blob/main/public/Project%20ScreenShots/Screenshot%20(67).png)
![Dark Mode](https://github.com/ManishTirkey/Face-Recognition-for-Attendance-/blob/main/public/Project%20ScreenShots/Screenshot%20(66).png) 


## [CustomTkinter](https://customtkinter.tomschimansky.com/documentation/) based Facial Recognition for Attendance.
## :seedling: Getting Started

#### Download MySql [Mysql](https://dev.mysql.com/downloads/installer/)

+ To run this code use by 
```
https://github.com/ManishTirkey/Face-Recognition-for-Attendance.git
cd Face-Recognition-for-Attendance
python -m venv Face_Recognition_ENV
Face_Recognition_ENV\Scripts\activate
pip install -r requirements.txt.
```
Before running the Project make sure you have configured database host, password and and database name into `DB_config.py`

+ `go to public` and run `python DB_initialize.py` (DB_config.py does all the configuration for you.)
+ Run `python App.py` this will run the program.

if something goes wrong you can clean the project by resetting the database and trained.yml and images.
```
python Clean_data.py
```

## :motorcycle: Other Repositories
- [Youtube Video Download App](https://github.com/ManishTirkey/Download_youtube_Videos)
  - Both Audio and video separately.
- [Control Volume with hand Gesture](https://github.com/ManishTirkey/Volume_control_opencv)
- [Screenshot Application](https://github.com/ManishTirkey/ScreenShot)
  - ElectonJS and python based Screenshot Application.
  - window sticks on top of window application.
  - Take screenshots of the particular area.
