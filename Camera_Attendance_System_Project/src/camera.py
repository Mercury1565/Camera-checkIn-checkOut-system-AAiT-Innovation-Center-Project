import cv2
import time
from pathlib import Path

class Camera:
    def __init__(self, camera_index=0, save_directory="data/faces/"):
        """
        Initialize the Camera class to use a webcam.
        
        :param camera_index: The index of the camera (0 for default, 1 for external)
        :param save_directory: Directory where captured images will be saved
        """
        self.camera = cv2.VideoCapture(camera_index)
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(parents=True, exist_ok=True)

        if not self.camera.isOpened():
            raise Exception("Could not open webcam")

    def capture_image(self, name, user_id):
        """
        Captures an image using the webcam and saves it to the specified directory.
        
        :param filename: The name of the file to save the image as (default: timestamp-based)
        :return: The path to the saved image
        """
        filename = f"{user_id}_{name}_{int(time.time())}.jpg"
        image_path = self.save_directory / filename
                
        # Capture a frame from the webcam
        ret, frame = self.camera.read()

        if not ret:
            raise Exception("Failed to capture image from webcam")
        
        # Save the captured frame to the specified path
        cv2.imwrite(str(image_path), frame)
        
        return image_path

    def show_live_feed(self, process_frame_callback=None, duration = 3):
        """
        Displays a live video feed from the webcam until the user presses 'q' to quit.
        """
        print("Starting live video feed. Press 'q' to exit.")

        start_time = time.time()
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame.")
                break

            if process_frame_callback:
                frame = process_frame_callback(frame)
            
            cv2.imshow('Live Feed', frame)            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            elapsed_time = time.time() - start_time
            if elapsed_time > duration:
                break
        
        cv2.destroyAllWindows()
        print("Live feed ended.")

    def close(self):
        """
        Release the webcam resource.
        """
        self.camera.release()
        print("Webcam resource released.")