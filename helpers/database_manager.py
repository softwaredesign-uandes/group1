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

	def insert_new_mineral_deposit(self, data_file):
		file = open(data_file)
		data = file.readline().strip().split(',')
		name = data[0]
		minerals = data[1:]
		self.db.mineral_deposits.insert_one({ "name": name, "minerals": minerals })

	def fetch_mineral_deposit(self, mineral_deposit):
		return self.db.mineral_deposits.find_one({ "name": mineral_deposit })

	def insert_new_block_model(self, mineral_deposit_name, headers_file):
		headers = parse_headers(headers_file)
		mineral_deposit = self.fetch_mineral_deposit(mineral_deposit_name)
		data_map = self.map_headers(headers, mineral_deposit["minerals"])
		name = ""
		while name == "":
			name = input("What would you like to name this block model?\n>>> ")
			if self.fetch_block_model(mineral_deposit_name, name) != None:
				print("A block model with that name already exist within this mineral deposit.")
				name = ""
		self.db.block_models.insert_one({ "name": name, "mineral_deposit_name": mineral_deposit_name, "headers": headers, "data_map": data_map })

	def fetch_block_model(self, mineral_deposit, block_model):
		return self.db.block_models.find_one({ "name": block_model, "mineral_deposit_name": mineral_deposit })

	def insert_blocks(self, mineral_deposit, block_model, data_file):
		model = self.fetch_block_model(mineral_deposit, block_model)
		headers = model["headers"]
		amount_headers = len(headers)
		data = parse_file(data_file)
		data_map = model["data_map"]
		weight_column = data_map["weight"]
		weight_column_index = headers.index(weight_column)
		grades_data_map = data_map["grade"]
		data_array = []
		my_units = {}
		grade_units = ['tonn', 'percentage', 'oz/tonn', 'ppm']
		print("In which of the following units is each of the grades:")
		for index in range(len(grade_units)):
			print("\t{}. {}".format(index + 1, grade_units[index]))
		for grade in grades_data_map:
			print("{}: ".format(grade), end = '')
			unit_index = self.get_valid_index(grade_units) - 1
			my_units[grades_data_map[grade]] = unit_index
		for item in data:
			document = { "mineral_deposit": mineral_deposit, "block_model": block_model }
			for index in range(amount_headers):
				if headers[index] in grades_data_map.values():
					transformed = self.grade_to_percentage(item[index], item[weight_column_index], grade_units[my_units[headers[index]]])
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

	def map_headers(self, headers, minerals):
		data_map = {}
		print("You have entered the following headers for your block model:")
		for index in range(len(headers)):
			print("\t{}. {}".format(index + 1, headers[index]))
		print("Please tell me, which one of those hearders refers to:")
		relevant_headers = ['x', 'y', 'z', 'weight']
		for header in relevant_headers:
			print("{}: ".format(header), end = '')
			response = self.get_valid_index(headers) - 1
			data_map[header] = headers[response]
		data_map["grade"] = {}
		for mineral in minerals:
			print("{} grade: ".format(mineral), end = '')
			response = self.get_valid_index(headers) - 1
			data_map["grade"][mineral] = headers[response]
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
		else:
			return value

	def get_max_x_y_z_value(self, mineral_deposit_name, block_model_name):
		block_model = self.db.block_models.find_one({"mineral_deposit_name": mineral_deposit_name, "name": block_model_name})
		x = block_model["data_map"]["x"]
		y = block_model["data_map"]["y"]
		z = block_model["data_map"]["z"]
		block_max_x = self.db.blocks.find().sort({x: -1}).limit(1)
		block_max_y = self.db.blocks.find().sort({y: -1}).limit(1)
		block_max_z = self.db.blocks.find().sort({z: -1}).limit(1)
		return block_max_x[x], block_max_y[y], block_max_z[z]
