import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not configured in .env")

client = MongoClient(MONGO_URI)

db = client["receptionist_db"]

faculty_collection = db["faculty"]
appointments_collection = db["appointments"]
availability_collection = db["availability"]

# Faculty indexes
faculty_collection.create_index("faculty_id", unique=True)
faculty_collection.create_index("name")
faculty_collection.create_index("department")


# Availability indexes
availability_collection.create_index(
    [("faculty_id", 1), ("date", 1)],
    unique=True
)


# Appointment indexes
appointments_collection.create_index(
    "appointment_id",
    unique=True
)

appointments_collection.create_index(
    [
        ("student_id", 1),
        ("date", 1),
        ("time", 1),
        ("status", 1)
    ]
)

appointments_collection.create_index(
    [
        ("faculty_id", 1),
        ("date", 1),
        ("time", 1),
        ("status", 1)
    ]
)