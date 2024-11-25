import os
import time
import cv2
import numpy as np
from pathlib import Path
from deepface import DeepFace

class FaceRecognition:
    def __init__(self, directory="data/faces/"):
        """
        Initialize DeepFace-based face recognition.
        """
        self.face_data_directory = Path(directory)
        self.face_data_directory.mkdir(parents=True, exist_ok=True)
        self.known_faces = {}
        self._load_known_faces()

    def register_face(self, frame, name, user_id):
        """
        Register a new face by saving the image and updating embeddings.
        """
        recognized_face, embedding = self.recognize_face_from_frame(frame)

        if not recognized_face:
            file_name = self._save_image(frame, name, user_id)
            name = file_name.split('.')[0]
            self.known_faces[name] = embedding

        return recognized_face

    def recognize_face_from_frame(self, frame):
        """
        Recognize faces in a frame using DeepFace.
        """
        # Preprocess the frame (DeepFace requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Generate embedding for the current frame
        frame_embedding = self._get_embedding(rgb_frame)

        # Compare with known faces
        recognized_face = self._match_face(frame_embedding)
        return recognized_face, frame_embedding

    def _get_embedding(self, image):
        """
        Get the embedding of an image using DeepFace.
        """
        embedding = DeepFace.represent(img_path=image, model_name="Facenet",  enforce_detection=False)[0]["embedding"]
        return embedding

    def _match_face(self, face_embedding):
        """
        Compare the face embedding with known embeddings.
        """

        # Perform face embedding calculation
        best_match, min_dist = self._compare_face_thresholds(face_embedding)

        # Set threshold
        if best_match and min_dist < 0.8:
            print(f"Best match: {best_match}, Min distance: {min_dist}")
            return best_match

        return 

    def _compare_face_thresholds(self, face_embedding):
        min_distance = float('inf')
        best_match = None

        for name, known_embedding in self.known_faces.items():
            face_embedding = face_embedding / np.linalg.norm(face_embedding)
            known_embedding = known_embedding / np.linalg.norm(known_embedding)

            distance = np.linalg.norm(face_embedding - known_embedding)
            print(f"Comparing with {name}: Distance = {distance}")

            if distance < min_distance:
                min_distance = distance
                best_match = name

        return best_match, min_distance


    def _load_known_faces(self):
        """
        Load all known faces and compute embeddings if not already loaded.
        """
        
        for file_name in os.listdir(self.face_data_directory):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                name = file_name.split('.')[0]
                image_path = self.face_data_directory / file_name

                # Generate and store embedding
                embedding = self._get_embedding(str(image_path))
                self.known_faces[name] = embedding

    def _save_image(self, frame, name, user_id):
        """
        Save a frame to the specified directory with metadata.
        """
        filename = f"{user_id}_{name}_{int(time.time())}.jpg"
        image_path = self.face_data_directory / filename

        # Save the frame in RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(str(image_path), rgb_frame)

        return filename
