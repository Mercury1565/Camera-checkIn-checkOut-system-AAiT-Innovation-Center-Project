from fastapi import FastAPI, UploadFile, File, Form
from src.face_recognition import FaceRecognition
import cv2
import numpy as np

app = FastAPI()
recognizer = FaceRecognition(directory="data/faces/")

@app.post("/recognize-face/")
async def recognize_face(
    file: UploadFile = File(...)
):
    try:
        # Read and decode the uploaded file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"error": "Invalid image data"}

        # Convert BGR to RGB (DeepFace expects RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face recognition
        recognized_name, embedding = recognizer.recognize_face_from_frame(frame_rgb)
        return {"name": recognized_name or None}

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/register-face/")
async def register_face(
    name: str = Form(...),  
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Read and decode the uploaded file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return {"error": "Invalid image data"}

        # Convert BGR to RGB (DeepFace expects RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Register the face
        registered_name = recognizer.register_face(frame_rgb, name, user_id)
        return {"name": registered_name or None}

    except Exception as e:
        return {"error": str(e)}


@app.get("/reload-known-faces/")
def reload_faces():
    recognizer.load_known_faces()
    return {"status": "Reloaded known faces"}
