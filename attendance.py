from pymongo import MongoClient
from datetime import datetime
import time
import json
import csv
import smtplib
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def createCSV(students):
    column_names = ['No', 'Name', 'Matric No']

    with open('Attendance.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader
        writer.writerows(students)

def sendEmail(attendance_file):
    my_email = os.getenv('EMAIL')
    recipient_email = os.getenv('EMAIL2')
    password_key = os.getenv('APP_PASSWORD')

    my_server = smtplib.SMTP_SSL('smtp.gmail.com')

    my_server.login(my_email, password_key)

    message = MIMEMultipart("alternative")

    with open(attendance_file, 'rb') as file:
        file = MIMEApplication(
            file.read(),
            name = os.path.basename(attendance_file)
        )
        file['Content-Disposition'] = 'attachment;'

        message.attach(file)

        my_server.sendmail(
            from_addr=my_email,
            to_addrs=recipient_email,
            msg=message.as_string()
        )

    my_server.quit()


def attendance(recognised_faces):
    client = MongoClient("mongodb://localhost:27017/")
    cctv_db = client['cctv_recognition']
    collection = cctv_db['attendance_system']
    present_students = {}
    present_students_array = []
    
    for i in range(1, len(recognised_faces)):
        present_students[i] = {
            "name": recognised_faces[i],
            "matric_no": 170408041
        }

        student_row = {
            "No": i,
            "Name": recognised_faces[i],
            "Matric No": "170408041"
        }
        
        unique_values = {d['Name'] for d in present_students_array}

        if student_row['Name'] not in unique_values:
            present_students_array.append(student_row)

    collection.insert_one({
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Time": time.strftime("%H:%M:%S", time.localtime()),
        "Present_Students": json.dumps(present_students)
    })

    createCSV(present_students_array)
    file = 'Attendance.csv'
    sendEmail(file)


