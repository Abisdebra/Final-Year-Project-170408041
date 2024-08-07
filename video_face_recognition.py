import os
import face_recognition
import pickle
import numpy as np
import cv2
from send_message import send_message
from attendance import attendance

def encode_faces(folder_path):
    face_encodings = {}
    for person_name in os.listdir(folder_path):
        person_folder = os.path.join(folder_path, person_name)
        if not os.path.isdir(person_folder):
            continue
        encodings = []
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)
            image = face_recognition.load_image_file(image_path)
            enc = face_recognition.face_encodings(image, num_jitters=100)

            if len(enc) > 0:
                encodings.append(enc[0])
        if encodings:
            face_encodings[person_name] = encodings
    with open('face_encodings.pkl', 'wb') as f:
        pickle.dump(face_encodings, f)

if not os.path.exists('face_encodings.pkl'):
    encode_faces('face_database')

with open('face_encodings.pkl', 'rb') as f:
    face_encodings = pickle.load(f)

webcam = cv2.VideoCapture(0)
recognised_faces = []

def recognise_faces_in_frame(frame):
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        print("No faces found in the frame.")
        return
    
    face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_in_frame):
        matches = []
        for person_name, encodings in face_encodings.items():
            results = face_recognition.compare_faces(encodings, face_encoding, tolerance=0.4)
            if any(results):
                matches.append(person_name)
        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        if matches:
            name = matches[0]
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            recognised_faces.append(name)
            send_message(name)
        else:
            cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

process_this_frame = True

while True:
    ret, frame = webcam.read()

    if not ret:
        print("Failed to grab frame")
        break

    if process_this_frame:
        recognise_faces_in_frame(frame)

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if(len(recognised_faces) > 0):
            attendance(recognised_faces)
        recognised_faces = []
        break

webcam.release()
cv2.destroyAllWindows()


        