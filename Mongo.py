from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import pytz

# Constants
DB_NAME = "test"  # Database name
CONNECTION_URL = (
    "mongodb+srv://leilanunez01:csulbCECS327@cluster0.q6mnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)  # Database URL
SENSOR_TABLE = "Table1_virtual"  #Sensor table data

def query_to_list(cursor):
    """Convert a MongoDB query cursor to a list."""
    return list(cursor)

def convert_to_pst(utc_time):
    utc_dt = utc_time.replace(tzinfo=pytz.utc)  # Ensure UTC timezone because Mongo is timestamped in UTC
    pst_dt = utc_dt.astimezone(pytz.timezone('US/Pacific'))  # Convert to PST
    return pst_dt.strftime('%Y-%m-%d %H:%M:%S')  # Format as a string

def query_database_with_metadata(collection_name, field, asset_id=None, start_time=None, end_time=None):
    try:
        client = MongoClient(CONNECTION_URL, tlsCAFile=certifi.where())
        db = client[DB_NAME]
        collection = db[collection_name]

        pipeline = [
            {
                '$lookup': {
                    'from': 'Table1_metadata',  # Join with the 'Table1_metadata' collection
                    'localField': 'payload.parent_asset_uid', 
                    'foreignField': 'assetUid',
                    'as': 'metadata'  # Output array field name for the joined documents
                }
            },
            {
                '$unwind': {
                    'path': '$metadata',  # Deconstruct the 'metadata' array field
                    'preserveNullAndEmptyArrays': True  # Keep documents without metadata
                }
            },
            {
                '$match': {
                    f"payload.{field}": {'$exists': True},  # Filter documents
                    **({'metadata.assetUid': asset_id} if asset_id else {}),
                    'time': {'$gte': start_time, '$lte': end_time}  # Filter documents by time range for queries like #1
                }
            }
        ]

        documents = collection.aggregate(pipeline)
        docs = list(documents)
        # print("Documents:", docs)

        for doc in docs:
            if 'time' in doc:
                doc['time_pst'] = convert_to_pst(doc['time']) 

        return [doc["payload"][field] for doc in docs]

    except Exception as e:
        print("Error: Unable to connect or query MongoDB.")
        print(f"Details: {e}")
        exit(1)