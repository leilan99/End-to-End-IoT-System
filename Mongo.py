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
        collection = db[collection_name]
        print(f"Using collection: {collection_name}")

        # Set time cutoff for filtering documents
        time_cutoff = datetime.now() - timedelta(hours=hours)

        # Query documents
        query = {
            "topic": topic,
            "time.$date": {"$gte": time_cutoff.timestamp() * 1000}  # Convert to milliseconds
        }
        documents = query_to_list(collection.find(query))

        if field:
            # Extract only the specified field if provided
            documents = [doc.get("payload", {}).get(field) for doc in documents if "payload" in doc]

        return documents

    except Exception as e:
        print("Error: Unable to connect or query MongoDB.")
        print("Ensure that this machine's IP has access to MongoDB.")
        print(f"Details: {e}")
        exit(1)