from database import client, db

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
    print(f"Database: {db.name}")

except Exception as e:
    print("MongoDB connection failed!")
    print(e)

finally:
    client.close()