from database import retrive_info
from sms_notif import send_sms
from pymongo import MongoClient
from datetime import datetime, timedelta

RECIPIENT = "+2348133357342"

def send_message(name):
    message = retrive_info(name)

    if message:
        client = MongoClient("mongodb://localhost:27017/")
        cctv_db = client['cctv_recognition']
        collection = cctv_db['sent_messages']

        last_message_entry = collection.find_one(sort = [('timestamp', -1)])

        if last_message_entry:
            last_message = last_message_entry["message"]
            last_timestamp = last_message_entry["timestamp"]

            if message == last_message:
                elapsed_time = datetime.now() - last_timestamp
                if elapsed_time < timedelta(minutes = 10):
                    print("Message already sent within the last 10 minutes. Not sent!")
                    return False  
        
        collection.insert_one({
            "message": message,
            "timestamp": datetime.now()
        })
        print(message)
        send_sms(RECIPIENT, message)
        return True
