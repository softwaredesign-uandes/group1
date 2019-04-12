from pymongo import MongoClient
import helpers.connection_params as params
from helpers.file_parser import parse_file, parse_headers


class Manager():
	def __init__(self):
		connection = MongoClient(
	        'mongodb://{user}:{password}@{host}:'
	        '{port}/{namespace}'.format(**params.CONNECTION_PARAMS)
	    )
		self.db = connection

	def insert_new_mineral_deposit(self, mineral_deposit):
		name = ""
		while name == "":
			name = input("What would you like to name this mineral deposit?\n>>> ")
			if self.fetch_mineral_deposit(mineral_deposit).limit(1).count() != 0:
				print("A mineral deposit with that name already exist.")
				name = ""
		self.db.mineral_deposits.insert_one({ "name": mineral_deposit })

	def fetch_mineral_deposit(self, mineral_deposit):
		return self.db.mineral_deposits.find({ "name": mineral_deposit })

	def insert_new_block_model(self, mineral_deposit, headers_file):
		headers = parse_headers(headers_file)
		name = ""
		while name == "":
			name = input("What would you like to name this block model?\n>>> ")
			if self.fetch_block_model(mineral_deposit, name).limit(1).count() != 0:
				print("A block model with that name already exist within this mineral deposit.")
				name = ""
		self.db.block_models.insert_one({ "name": name, "mineral_deposit_name": mineral_deposit, "headers": headers })

	def fetch_block_model(self, mineral_deposit, block_model):
		return self.db.block_models.find({ "name": block_model, "mineral_deposit_name": mineral_deposit })

	def insert_blocks(self, mineral_deposit, block_model, data_file):
		model = self.fetch_block_model(mineral_deposit, block_model)
		headers = model["headers"]
		amount_headers = len(headers)
		data = parse_file(data_file)
		data_array = []
		for item in data:
			document = { "mineral_deposit": mineral_deposit, "block_model": block_model }
			for index in range(amount_headers):
				document[headers[index]] = item[index]
			data_array.append(document)
		self.db.blocks.insert_many(data_array)

	def find_by_coordinates(self, mineral_deposit, block_model, coordinates_string):
		coordinates = [int(x) for x in coordinates_string.strip().split(',')]
		return self.db.blocks.find({ "mineral_deposit_name": mineral_deposit, "block_model": block_model, "x": coordinates[0],"y": coordinates[1],"z": coordinates[2] })

	def get_all_blocks_from_block_model(self, mineral_deposit, block_model):
		return self.db.blocks.find({ "mineral_deposit": mineral_deposit, "block_model": block_model })


	def remove_all_blocks_from_block_model(self, mineral_deposit, block_model):
		return self.db.blocks.remove({ "mineral_deposit_name": mineral_deposit, "block_model": block_model })
