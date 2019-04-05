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
	if find_by_coordinates(db, block.id, block.model).limit(1).count() == 0:
		db.blocks.insert_one(block.as_json())

def insert_many(db, blocks):
	db.blocks.insert_many(blocks)

def find_by_coordinates(db, x,y,z, model):
    return db.blocks.find({"x": x,"y": y,"z": z, "model": model })

def get_model_blocks(db, model):
	return db.blocks.find({ "model": model })

def print_block(response):
	block = Block(response['model'], response['id'], response['x'], response['y'], response['z'], response['weight'], response['grade'])
	print(block)

def remove_model_blocks(db, model):
	return db.blocks.remove({ "model": model })
