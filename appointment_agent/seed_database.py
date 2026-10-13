from database import faculty_collection, availability_collection

faculty = [
    {
        "faculty_id": "F001",
        "name": "Dr. Ravi Kumar",
        "department": "Computer Science",
        "designation": "Professor"
    },
    {
        "faculty_id": "F002",
        "name": "Dr. Anitha Sharma",
        "department": "Information Science",
        "designation": "Associate Professor"
    },
    {
        "faculty_id": "F003",
        "name": "Dr. Mahesh Rao",
        "department": "Electronics",
        "designation": "Professor"
    }
]


# Prevent duplicate faculty records
for member in faculty:
    faculty_collection.update_one(
        {"faculty_id": member["faculty_id"]},
        {"$set": member},
        upsert=True
    )

print("Faculty data inserted successfully.")

for member in faculty_collection.find({}, {"_id": 0}):
    print(member)

availability = [
    {
        "faculty_id": "F001",
        "date": "2026-10-02",
        "slots": ["10:00", "11:30", "14:00", "16:00"]
    },
    {
        "faculty_id": "F001",
        "date": "2026-10-03",
        "slots": ["09:30", "11:00", "14:30"]
    },
    {
        "faculty_id": "F002",
        "date": "2026-10-02",
        "slots": ["09:00", "12:00", "15:00"]
    },
    {
        "faculty_id": "F002",
        "date": "2026-10-03",
        "slots": ["10:00", "13:00", "16:00"]
    },
    {
        "faculty_id": "F003",
        "date": "2026-10-02",
        "slots": ["10:30", "13:30", "15:30"]
    },
    {
        "faculty_id": "F003",
        "date": "2026-10-03",
        "slots": ["09:00", "11:30", "14:00"]
    }
]


for availability_record in availability:
    availability_collection.update_one(
        {
            "faculty_id": availability_record["faculty_id"],
            "date": availability_record["date"]
        },
        {
            "$set": availability_record
        },
        upsert=True
    )

print("Availability data inserted successfully.")