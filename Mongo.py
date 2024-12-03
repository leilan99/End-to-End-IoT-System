from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi

# Constants
DB_NAME = "test"  # Change to your database name
CONNECTION_URL = (
    "mongodb+srv://leilanunez01:csulbCECS327@cluster0.q6mnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)  # Replace with your database URL
SENSOR_TABLE = "Table1_virtual"  #Sensor table data

def query_to_list(cursor):
    """Convert a MongoDB query cursor to a list."""
    return list(cursor)

def query_database(collection_name, topic=None, field=None, hours=3):
    try:
        client = MongoClient(CONNECTION_URL, tlsCAFile=certifi.where())
        db = client[DB_NAME]

        # Access the specified collection
        collection = db[SENSOR_TABLE]
        print(f"Using collection: {SENSOR_TABLE}")

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        query = {
            "topic": topic,
            "time": {"$gte": start_time, "$lte": end_time},
            f"payload.{field}": {"$exists": True}
        }
        documents = collection.find(query)
        return [doc["payload"][field] for doc in documents]

    except Exception as e:
        print("Error: Unable to connect or query MongoDB.")
        print("Ensure that this machine's IP has access to MongoDB.")
        print(f"Details: {e}")
        exit(1)