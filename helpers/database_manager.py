from pymongo import MongoClient
import helpers.connection_params as params
from helpers.file_parser import parse_file, parse_headers


class Manager():
	def __init__(self):
		connection = MongoClient(
	        'mongodb://{user}:{password}@{host}:'
	        '{port}/{namespace}'.format(**params.CONNECTION_PARAMS)
	    )
		self.db = connection.mining_blocks

	def insert_new_mineral_deposit(self):
		name = ""
		while name == "":
			name = input("What would you like to name this mineral deposit?\n>>> ")
			if self.fetch_mineral_deposit(name).limit(1).count() != 0:
				print("A mineral deposit with that name already exist.")
				name = ""
		self.db.mineral_deposits.insert_one({ "name": name })

	def fetch_mineral_deposit(self, mineral_deposit):
		return self.db.mineral_deposits.find_one({ "name": mineral_deposit })

	def insert_new_block_model(self, mineral_deposit, headers_file):
		headers = parse_headers(headers_file)
		data_map = self.map_headers(headers)
		name = ""
		while name == "":
			name = input("What would you like to name this block model?\n>>> ")
			if self.fetch_block_model(mineral_deposit, name) != None:
				print("A block model with that name already exist within this mineral deposit.")
				name = ""
		self.db.block_models.insert_one({ "name": name, "mineral_deposit_name": mineral_deposit, "headers": headers, "data_map": data_map })

	def fetch_block_model(self, mineral_deposit, block_model):
		return self.db.block_models.find_one({ "name": block_model, "mineral_deposit_name": mineral_deposit })

	def insert_blocks(self, mineral_deposit, block_model, data_file):
		model = self.fetch_block_model(mineral_deposit, block_model)
		headers = model["headers"]
		amount_headers = len(headers)
		data = parse_file(data_file)
		data_map = model["data_map"]
		weight_column_index = data_map["weight"]
		grade_column_index = data_map["grade"]
		data_array = []
		grade_units = ['tonn', 'percentage', 'oz/tonn', 'ppm']
		print("In which of the following units is your grade:")
		for index in range(len(grade_units)):
			print("\t{}. {}".format(index + 1, grade_units[index]))
		unit_index = self.get_valid_index(grade_units) - 1
		my_unit = grade_units[unit_index]
		for item in data:
			document = { "mineral_deposit": mineral_deposit, "block_model": block_model }
			for index in range(amount_headers):
				if index == grade_column_index:
					transformed = self.grade_to_percentage(item[index], item[weight_column_index], my_unit)
					item[index] = transformed
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

	def map_headers(self, headers):
		data_map = {}
		print("You have entered the following headers for your block model:")
		for index in range(len(headers)):
			print("\t{}. {}".format(index + 1, headers[index]))
		print("Please tell me, which one of those hearders refers to:")
		relevant_headers = ['x', 'y', 'z', 'weight', 'grade']
		for header in relevant_headers:
			print("{}: ".format(header), end = '')
			response = self.get_valid_index(headers) - 1
			data_map[header] = headers[response]
		return data_map

	def get_valid_index(self, data):
		response = -1
		while response > len(data) or response <= 0:
			try:
				response = int(input())
			except:
				f = input("exit? y/n\n")
				if f == 'y':
					exit()
				continue
		return response

	def grade_to_percentage(self, value, weight, unit):
		if unit == 'tonn':
			return value / weight
		elif unit == 'oz/tonn':
			return value * 32000 / weight
		elif unit == 'ppm':
			return value / 10000
				