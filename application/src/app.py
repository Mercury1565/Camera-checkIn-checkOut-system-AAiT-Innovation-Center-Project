from src.camera import Camera
# from Face_Recognition_Model_Serve.face_recognition import FaceRecognition
import cv2
import requests
import tempfile

from src.database import Database

DATABASE_NAME= 'perago'
DATABASE_USER= 'mercury'
DATABASE_PASSWORD= 'herget123'

class App:
    def __init__(self):
        self.camera = Camera(camera_index=0)
        self.name = ''
        self.database = Database(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)

    def process_frame(self, frame):
        """
        Callback function to process each frame from the live feed.
        :param frame: The current frame captured from the live feed.
        :return: The frame with overlay text showing recognized person's name.
        """
        # Overlay recognized name on the frame
        if self.name:
            cv2.putText(frame, f"Recognized: {self.name.split('_')[1]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Face not recognized", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return frame

    def register_person(self, first_name, last_name, phone):
        temp_frame = self.camera.get_frame()
        self.name = self.recognize_face(temp_frame)

        frame = self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if self.name:
            print("Person already exists")
        else:
            user_id = self.database.register_user(first_name=first_name, last_name=last_name, phone=phone)
            self.name = self.register_face(frame, first_name, user_id)
            print('User registered successfully !!!')
                
    def check_in(self):
        temp_frame = self.camera.get_frame()
        self.name = self.recognize_face(temp_frame)

        frame = self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if not self.name:
            print('User not found, register first')
        else:
            user_id = self.name.split('_')[0]
            first_name, last_name, checked_in = self.database.check_in(int(user_id))
            
            if not checked_in:
                print(f"{first_name}  {last_name} is already checked in.")
            else:
                print(f'{first_name} {last_name} has checked in successfully!')
    
    def check_out(self):
        temp_frame = self.camera.get_frame()
        self.name = self.recognize_face(temp_frame)

        frame = self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if not self.name:
            print('User not found, register first')
        else:
            user_id = self.name.split('_')[0]
            first_name, last_name, checked_in = self.database.check_out(int(user_id))

            if not checked_in:
                print(f"{first_name} {last_name} is not checked in.")
            else:
                print(f'{first_name} {last_name} has checked out successfully!')

    def recognize_face(self, frame):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
            temp_path = temp_image_file.name
            cv2.imwrite(temp_path, frame)

        with open(temp_path, "rb") as img_file:
            response = requests.post(
            "http://localhost:8000/recognize-face/",
            files={"file": ("image.jpg", img_file)},
            )

        return response.json().get('name')
    
    def register_face(self, frame, name, user_id):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
            temp_path = temp_image_file.name
            cv2.imwrite(temp_path, frame)

        with open(temp_path, "rb") as img_file:
            response = requests.post(
            "http://localhost:8000/register-face/",
            files={"file": ("image.jpg", img_file)},
            data={"name": name, "user_id": user_id}
            )

        return response.json().get('name')

    
    def _admin_confirmation(self):
        self.camera.show_live_feed(process_frame_callback=self.process_frame, duration=10)

        if not self.name:
            return False
        else:
            user_id = self.name.split('_')[0]
            is_admin = self.database.check_if_admin(user_id)

            if not is_admin:
                return False

        return True

    # def remove_person(user_id):
