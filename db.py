from pymongo import MongoClient
from datetime import datetime, timezone
import time
import os
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["website-hub-auth"]

users_collection = db["users"]
otps_collection = db["otps"]
sessions_collection = db["sessions"]

# def storeUserData():
#     users_collection.insert_one({
#         "email": "example@gmail.com",
#         "phone_number": 9232323232,
#         "creationDate": datetime.now(timezone.utc),
#         "lastLoginAt": None,
#         "isActive": True
#     })

def storeOTP(phonenum,email,otp):
    if phonenum is not None:
        query_filter = {"phone_number": phonenum}
    elif email is not None:
        query_filter = {"email": email}
    else:
        print("Error: Must provide an identifier (phone or email).")
        return None

    update_payload = {
        "$set": {
            "phone_number": phonenum,
            "email": email,
            "otp": otp,
            "creationDate": datetime.now(timezone.utc)
        }
    }
    otps_collection.update_one(query_filter, update_payload, upsert=True)
    print("OTP stored or updated.")


def getOTP(identifier):
    if isinstance(identifier,int):
        query = {"phone_number": identifier}
    elif isinstance(identifier,str):
        query = {"email": identifier}
    else:
        return None
    return otps_collection.find_one(query)
    

def deleteOTP(phonenum,email):
    if phonenum is not None:
        query_filter = {"phone_number": phonenum}
    elif email is not None:
        query_filter = {"email": email}
    else:
        print("No identifier provided to delete.")
        return None
    result = otps_collection.delete_one(query_filter)
    if result.deleted_count > 0:
        print("OTP document deleted.")
    else:
        print("No matching document found to delete.")