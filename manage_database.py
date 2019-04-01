from pymongo import MongoClient
import connection_params

def get_connection():
    connection = MongoClient(
        'mongodb://{user}:{password}@{host}:'
        '{port}/{namespace}'.format(**connection_params.CONNECTION_PARAMS)
    )
    return connection.mining_blocks
def insert_one_block(db, block):

    db.blocks.insert_one(block.as_json())

def find_by_id(db, id):
    return db.find({"id": id })