from .database import (
    faculty_collection,
    availability_collection,
    appointments_collection
)

from datetime import datetime

def get_current_date() -> dict:
    """Return the current date in YYYY-MM-DD format."""

    today = datetime.now().astimezone().date()

    return {
        "status": "success",
        "current_date": today.isoformat()
    }

def search_faculty(name: str = "", department: str = "") -> dict:
    """Search faculty members by name or department.
    
    """

    query = {}

    if name:
        query["name"] = {
            "$regex": name,
            "$options": "i"
        }

    if department:
        query["department"] = {
            "$regex": department,
            "$options": "i"
        }

    results = list(
        faculty_collection.find(
            query,
            {"_id": 0}
        )
    )

    return {
        "status": "success",
        "count": len(results),
        "faculty": results
    }

def check_availability(
    faculty_id: str,
    date: str
) -> dict:
    """
    Check available appointment slots for a faculty member
    on a specific date.

    Date format: YYYY-MM-DD
    """

    availability = availability_collection.find_one(
        {
            "faculty_id": faculty_id,
            "date": date
        },
        {
            "_id": 0
        }
    )

    if availability is None:
        return {
            "status": "success",
            "faculty_id": faculty_id,
            "date": date,
            "available": False,
            "available_slots": [],
            "message": "No appointment slots are available on this date."
        }

    slots = availability.get("slots", [])

    if not slots:
        return {
            "status": "success",
            "faculty_id": faculty_id,
            "date": date,
            "available": False,
            "available_slots": [],
            "message": "No appointment slots are available on this date."
        }

    return {
        "status": "success",
        "faculty_id": faculty_id,
        "date": date,
        "available": True,
        "available_slots": slots
    }

def book_appointment(
    student_id: str,
    faculty_id: str,
    date: str,
    time: str,
    purpose: str
) -> dict:
    """
    Book an appointment with a faculty member.
    """

    # Check whether the faculty exists
    faculty = faculty_collection.find_one(
        {"faculty_id": faculty_id}
    )

    if faculty is None:
        return {
            "status": "error",
            "message": "Faculty member not found."
        }

    # Check whether the requested slot exists
    availability = availability_collection.find_one(
        {
            "faculty_id": faculty_id,
            "date": date
        }
    )

    if availability is None or time not in availability.get("slots", []):
        return {
            "status": "error",
            "message": "The requested time slot is not available."
        }

    # Check whether the student already has an appointment
    existing_appointment = appointments_collection.find_one(
        {
            "student_id": student_id,
            "date": date,
            "time": time,
            "status": "confirmed"
        }
    )

    if existing_appointment:
        return {
            "status": "error",
            "message": "You already have an appointment at this date and time."
        }

    # Create appointment ID
    appointment_count = appointments_collection.count_documents({})

    appointment_id = f"APT{appointment_count + 1:03d}"

    appointment = {
        "appointment_id": appointment_id,
        "student_id": student_id,
        "faculty_id": faculty_id,
        "date": date,
        "time": time,
        "purpose": purpose,
        "status": "confirmed"
    }

    # Store appointment in MongoDB
    appointments_collection.insert_one(appointment)

    # Remove booked slot from MongoDB availability
    availability_collection.update_one(
        {
            "faculty_id": faculty_id,
            "date": date
        },
        {
            "$pull": {
                "slots": time
            }
        }
    )

    return {
        "status": "success",
        "message": "Appointment booked successfully.",
        "appointment": appointment
    }

def get_my_appointments(student_id: str) -> dict:
    """
    Retrieve all confirmed appointments belonging to a student.
    """

    appointments = list(
        appointments_collection.find(
            {
                "student_id": student_id,
                "status": "confirmed"
            },
            {
                "_id": 0
            }
        )
    )

    if not appointments:
        return {
            "status": "success",
            "count": 0,
            "appointments": [],
            "message": "You do not have any confirmed appointments."
        }

    return {
        "status": "success",
        "count": len(appointments),
        "appointments": appointments
    }

def cancel_appointment(
    student_id: str,
    appointment_id: str
) -> dict:
    """
    Cancel an existing appointment belonging to a student.
    """

    # Find the appointment in MongoDB
    appointment = appointments_collection.find_one(
        {
            "appointment_id": appointment_id,
            "student_id": student_id,
            "status": "confirmed"
        },
        {
            "_id": 0
        }
    )

    if appointment is None:
        return {
            "status": "error",
            "message": "Appointment not found or it has already been cancelled."
        }

    # Change appointment status
    appointments_collection.update_one(
        {
            "appointment_id": appointment_id
        },
        {
            "$set": {
                "status": "cancelled"
            }
        }
    )

    # Return the cancelled slot to availability
    availability_collection.update_one(
        {
            "faculty_id": appointment["faculty_id"],
            "date": appointment["date"]
        },
        {
            "$addToSet": {
                "slots": appointment["time"]
            }
        }
    )

    return {
        "status": "success",
        "message": "Appointment cancelled successfully.",
        "appointment": {
            **appointment,
            "status": "cancelled"
        }
    }