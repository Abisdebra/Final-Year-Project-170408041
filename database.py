from pymongo import MongoClient
from datetime import datetime

def retrive_info(name):
    client = MongoClient("mongodb://localhost:27017/")
    cctv_db = client['cctv_recognition']
    collection = cctv_db['recognised_individuals']

    query = {"Name": name}

    result = collection.find_one(query)
    
    if result is None:
        return result
    
    return {
        "Name": result["Name"],
        "Gender": result["Gender"],
        "Age": result["Age"],
        "Student": result["Student"],
        "Department": result["Department"],
        "Status": result["Status"],
        "Last_crime": result["Last_crime"],
        "Last_seen": result["Last_seen"],
        "Safety_Precautions": result["Safety_Precautions"]
    }
