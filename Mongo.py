from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi  # pip install certifi

# Constants
DB_NAME = "test"  # Change to your database name
CONNECTION_URL = (
    "mongodb+srv://leilanunez01:csulbCECS327@cluster0.q6mnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)  # Replace with your database URL
SENSOR_TABLE = "sensor data"  # Change this to your sensor data table
TIME_CUTOFF_MINUTES = 0  # Set how many minutes to allow for filtering

def query_to_list(cursor):
    """Convert a MongoDB query cursor to a list."""
    return list(cursor)

def query_database():
    """Query the database for sensor data."""
    try:
        # Connect to MongoDB
        client = MongoClient(CONNECTION_URL, tlsCAFile=certifi.where())
        db = client[DB_NAME]

        print("Database collections:", db.list_collection_names())

        # Access the specified sensor table
        sensor_table = db[SENSOR_TABLE]
        print("Using collection:", SENSOR_TABLE)

        # Set time cutoff for filtering documents
        time_cutoff = datetime.now() - timedelta(minutes=TIME_CUTOFF_MINUTES)

        # Query documents
        old_documents = query_to_list(sensor_table.find({"time": {"$gte": time_cutoff}}))
        current_documents = query_to_list(sensor_table.find({"time": {"$lte": time_cutoff}}))

        print("Current Docs:", current_documents)
        print("Old Docs:", old_documents)

        # Parse and return sensor data
        sensor_data = [
            (doc.get("sensor_id"), doc.get("value"))
            for doc in current_documents + old_documents
        ]
        return sensor_data

    except Exception as e:
        print("Error: Unable to connect or query MongoDB.")
        print("Ensure that this machine's IP has access to MongoDB.")
        print(f"Details: {e}")
        exit(1)

if __name__ == "__main__":
    sensor_data = query_database()
    print("Sensor Data:", sensor_data)
