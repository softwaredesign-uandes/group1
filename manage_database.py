from pymongo import MongoClient
import connection_params
from file_parser import parse_file, parse_headers

def get_connection():
    connection = MongoClient(
        'mongodb://{user}:{password}@{host}:'
        '{port}/{namespace}'.format(**connection_params.CONNECTION_PARAMS)
    )
    return connection.mining_blocks

def insert_new_mineral_deposit(db, mineral_deposit):
	name = ""
	while name == "":
		name = input("What would you like to name this mineral deposit?\n>>> ")
		if fetch_mineral_deposit(db, mineral_deposit).limit(1).count() != 0:
			print("A mineral deposit with that name already exist.")
			name = ""
	# WE HAVE TO CREATE A NEW COLLECTION IN OUR DATABASE CALLED "MINERAL_DEPOSITS"
	db.mineral_deposits.insert_one({ "name": mineral_deposit })

def fetch_mineral_deposit(db, mineral_deposit):
	return db.mineral_deposits.find({ "name": mineral_deposit })

def insert_new_block_model(db, mineral_deposit, headers_file):
	headers = parse_headers(headers_file)
	name = ""
	while name == "":
		name = input("What would you like to name this block model?\n>>> ")
		if fetch_block_model(db, mineral_deposit, name).limit(1).count() != 0:
			print("A block model with that name already exist within this mineral deposit.")
			name = ""
	# WE HAVE TO CREATE A NEW COLLECTION IN OUR DATABASE CALLED "BLOCK_MODELS"
	db.block_models.insert_one({ "name": name, "mineral_deposit_name": mineral_deposit, "headers": headers })

def fetch_block_model(db, mineral_deposit, block_model):
	# WE HAVE TO CREATE A NEW COLLECTION IN OUR DATABASE CALLED "BLOCK_MODELS"
	return db.block_models.find({ "name": block_model, "mineral_deposit_name": mineral_deposit })

def insert_blocks(db, mineral_deposit, block_model, data_file):
	model = fetch_block_model(db, mineral_deposit, block_model)
	headers = model["headers"]
	amount_headers = len(headers)
	data = parse_file(data_file)
	data_array = []
	for item in data:
		document = { "mineral_deposit": mineral_deposit, "block_model": block_model }
		for index in range(amount_headers):
			document[headers[index]] = item[index]
		data_array.append(document)
	db.blocks.insert_many(data_array)

def find_by_coordinates(db, mineral_deposit, block_model, coordinates_string):
	coordinates = [int(x) for x in coordinates_string.strip().split(',')]
	return db.blocks.find({ "mineral_deposit_name": mineral_deposit, "block_model": block_model, "x": coordinates[0],"y": coordinates[1],"z": coordinates[2] })

def get_all_blocks_from_block_model(db, mineral_deposit, block_model):
	return db.blocks.find({ "mineral_deposit": mineral_deposit, "block_model": block_model })


def remove_all_blocks_from_block_model(db, mineral_deposit, block_model):
	return db.blocks.remove({ "mineral_deposit_name": mineral_deposit, "block_model": block_model })
