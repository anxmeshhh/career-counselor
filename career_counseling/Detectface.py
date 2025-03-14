"""
@author: Santhosh R
"""
import cv2
import os
import csv
import pandas as pd

# Ensure necessary files exist
if not os.path.exists("Profile.csv"):
    print("🚨 Error: Profile.csv not found!")
    exit()

if not os.path.exists("haarcascade_frontalface_default.xml"):
    print("🚨 Error: Haarcascade file not found!")
    exit()

if not os.path.exists(r"TrainData/Trainner.yml"):
    print("🚨 Error: Trainner.yml file not found! Please train the model first.")
    exit()

# Remove duplicates from Profile.csv
df = pd.read_csv("Profile.csv")
df.sort_values("Ids", inplace=True)
df.drop_duplicates(subset="Ids", keep="first", inplace=True)
df.to_csv("Profile.csv", index=False)

# Function to detect face
def DetectFace():
    name_dict = {}

    # Read user profiles and store names by ID
    with open("Profile.csv", "r") as file:
        reader = csv.DictReader(file)
        print("🔍 Detecting Login Face...")

        for row in reader:
            name_dict[int(row["Ids"])] = row["Name"]

    # Load face recognizer and trained data
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainData/Trainner.yml")

    # Load Haarcascade file
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    Face_Id = "Not detected"

    # Camera ON
    while True:
        ret, frame = cam.read()
        if not ret:
            print("🚨 Error: Camera not detected!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        Face_Id = "Not detected"

        # Draw a rectangle around the face 
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 80 and Id in name_dict:
                Face_Id = name_dict[Id]
            else:
                Face_Id = "Unknown"
                
                # Save unknown faces
                unknown_faces_dir = "UnknownFaces"
                os.makedirs(unknown_faces_dir, exist_ok=True)
                noOfFile = len(os.listdir(unknown_faces_dir)) + 1
                
                if noOfFile < 100:
                    cv2.imwrite(os.path.join(unknown_faces_dir, f"Image{noOfFile}.jpg"), frame[y:y + h, x:x + w])

            cv2.putText(frame, Face_Id, (x, y + h + 30), font, 1, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)
        cv2.waitKey(1)

        # Checking if the face matches for Login
        if Face_Id == "Not detected":
            print("⚠️ Face Not Detected, Try again!")
        elif Face_Id != "Unknown":
            print(f"✅ Detected as {Face_Id}")
            print("🎉 Login Successful!")
            print(f"👋 Welcome {Face_Id}!")
            break
        else:
            print("❌ Login Failed, Please Try Again!")

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()

DetectFace()
