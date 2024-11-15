import dlib
import cv2
import os
import numpy as np
from pathlib import Path

class FaceRecognition:
    def __init__(self, face_data_directory="data/faces/"):
        """
        Initialize the FaceRecognition class with dlib.

        :param face_data_directory: Directory where known face images are stored.
        """
        self.face_data_directory = face_data_directory
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor("/home/mercury/Desktop/Innovation_Center_Project/Camera_Attendance_System_Project/src/shape_predictor_68_face_landmarks.dat")
        self.face_rec_model = dlib.face_recognition_model_v1("/home/mercury/Desktop/Innovation_Center_Project/Camera_Attendance_System_Project/src/dlib_face_recognition_resnet_model_v1.dat")
        self.known_faces = self._load_known_faces()

    def recognize_face_from_frame(self, frame):
        """
        Recognize the face in the given frame by comparing it to known faces in the database.
        :param frame: The frame containing the face to be recognized.
        :return: The name of the recognized person or NULL if no match is found.
        """
        # Convert frame to grayscale for better performance
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.detector(gray_frame)

        for face in faces:
            # Get the landmarks of the face
            shape = self.sp(gray_frame, face)
            
            # Get the face descriptor (128-Dimension vector)
            face_descriptor = self.face_rec_model.compute_face_descriptor(frame, shape)

            # Compare the descriptor with known faces
            name = self._match_face(face_descriptor)
            return name
        return None

    def _match_face(self, face_descriptor):
        """
        Compare the face descriptor with known faces.
        :param face_descriptor: The face descriptor of the frame.
        :return: The name of the recognized person or NULL if no match is found.
        """
        min_distance = float('inf')
        best_match = None

        for name, known_face in self.known_faces.items():
            # Calculate the distance between the input face descriptor and known faces
            distance = self._compute_face_distance(face_descriptor, known_face['descriptor'])
            if distance < min_distance:
                min_distance = distance
                best_match = name

        if best_match and min_distance < 0.8:
            return best_match
        return None

    def _compute_face_distance(self, face_descriptor1, face_descriptor2):
        """
        Compute the Euclidean distance between two face descriptors.
        :param face_descriptor1: The first face descriptor
        :param face_descriptor2: The second face descriptor
        :return: The Euclidean distance between the two descriptors
        """
        return np.linalg.norm(np.array(face_descriptor1) - np.array(face_descriptor2))

    def _load_known_faces(self):
        """
        Load all known faces from the database directory.
        :return: A dictionary where keys are the names of people and values are face descriptors.
        """
        known_faces = {}

        for file_name in os.listdir(self.face_data_directory):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                name = file_name.split('.')[0]
                image_path = os.path.join(self.face_data_directory, file_name)

                img = cv2.imread(image_path)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.detector(gray_img)

                if faces:
                    shape = self.sp(gray_img, faces[0])
                    face_descriptor = self.face_rec_model.compute_face_descriptor(img, shape)

                    known_faces[name] = {
                        'image': image_path,
                        'descriptor': face_descriptor
                    }

        return known_faces
