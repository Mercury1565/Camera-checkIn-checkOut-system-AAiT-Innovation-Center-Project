from src.camera import Camera
from src.face_recognition import FaceRecognition
import cv2

from src.database import Database

DATABASE_NAME= 'perago'
DATABASE_USER= 'mercury'
DATABASE_PASSWORD= 'herget123'

class App:
    def __init__(self):
        self.camera = Camera(camera_index=0)
        self.face_recognition = FaceRecognition()
        self.name = ''
        self.database = Database(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)

    def process_frame(self, frame):
        """
        Callback function to process each frame from the live feed.
        :param frame: The current frame captured from the live feed.
        :return: The frame with overlay text showing recognized person's name.
        """
        # Recognize the face in the current frame
        self.name = self.face_recognition.recognize_face_from_frame(frame)
        
        # Overlay recognized name on the frame
        if self.name:
            cv2.putText(frame, f"Recognized: {self.name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(f"Recognized person: {self.name}")
        else:
            cv2.putText(frame, "Face not recognized", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Face not recognized")

        return frame

    def register_person(self, first_name):
        self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if self.name:
            print("Person already exists")
        else:
            user_id = self.database.register_user(first_name=first_name)
            image_path = self.camera.capture_image(first_name, str(user_id))
            print(f"New image saved to {image_path}")
        
        self.camera.close()
        
    def check_in(self):
        self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if not self.name:
            print('User not found, register first')
        else:
            user_id = self.name.split('_')[0]
            self.database.check_in(int(user_id))
    
    def check_out(self):
        self.camera.show_live_feed(process_frame_callback=self.process_frame)

        if not self.name:
            print('User not found, register first')
        else:
            user_id = self.name.split('_')[0]
            self.database.check_out(int(user_id))
    
    # def remove_person(user_id):
