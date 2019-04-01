from pymongo import MongoClient
import connection_params
from blocks import Block

def get_connection():
    connection = MongoClient(
        'mongodb://{user}:{password}@{host}:'
        '{port}/{namespace}'.format(**connection_params.CONNECTION_PARAMS)
    )
    return connection.mining_blocks
def insert_one_block(db, block):
    db.blocks.insert_one(block.as_json())

def find_by_id(db, id, model):
    return db.blocks.find({"id": id, "model": model })

def get_model_blocks(db, model):
	return db.blocks.find({ "model": model })

def print_block(response):
	block = Block(response['model'], response['id'], response['x'], response['y'], response['z'], response['weight'], response['grade'])
	print(block)
