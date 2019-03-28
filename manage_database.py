from pymongo import MongoClient
import connection_params

def get_connection():
    connection = MongoClient(
        'mongodb://{user}:{password}@{host}:'
        '{port}/{namespace}'.format(**connection_params.CONNECTION_PARAMS)
    )
    return connection.mining_blocks

db = get_connection()
print(db.list_collection_names())