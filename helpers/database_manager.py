from pymongo import MongoClient
from .connection_params import CONNECTION_PARAMS as params
from .file_parser import parse_file, parse_headers
from .general_manager import GManager

class Manager:
	def __init__(self):
		connection = MongoClient(
	        'mongodb://{user}:{password}@{host}:'
	        '{port}/{namespace}'.format(**params)
	    )
		self.db = connection.mining_blocks
		self.gmanager = GManager()

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
		data_map = self.gmanager.map_headers(headers, mineral_deposit["minerals"])
		name = ""
		while name == "":
			name = input("What would you like to name this block model?\n>>> ")
			if self.fetch_block_model(mineral_deposit_name, name) != None:
				print("A block model with that name already exist within this mineral deposit.")
				name = ""
		self.db.block_models.insert_one({ "name": name, "mineral_deposit_name": mineral_deposit_name, "headers": headers, "data_map": data_map })

	def fetch_block_model(self, mineral_deposit, block_model):
		return self.db.block_models.find_one({ "name": block_model, "mineral_deposit_name": mineral_deposit })

	def get_params_from_model(self, model):
		headers = model["headers"]
		amount_headers = len(headers)
		data_map = model["data_map"]
		weight_column = data_map["weight"]
		weight_column_index = headers.index(weight_column)
		grades_data_map = data_map["grade"]
		return headers, amount_headers, data_map, weight_column, weight_column_index, grades_data_map

	def insert_blocks(self, mineral_deposit, block_model, data_file):
		model = self.fetch_block_model(mineral_deposit, block_model)
		headers, amount_headers, data_map, weight_column, weight_column_index, grades_data_map = self.get_params_from_model(model)
		data = parse_file(data_file)
		data_array = []
		grade_units = ['tonn', 'percentage', 'oz/tonn', 'ppm']
		self.print_units(grade_units)
		my_units = self.select_options_for_units(grade_units, grades_data_map)
		for item in data:
			document = self.create_block_document(mineral_deposit,block_model,amount_headers,headers,grades_data_map,item,weight_column_index,grade_units,my_units)
			data_array.append(document)
		self.db.blocks.insert_many(data_array)


	def print_units(self, grade_units):
		print("In which of the following units is each of the grades:")
		for index in range(len(grade_units)):
			print("\t{}. {}".format(index + 1, grade_units[index]))


	def select_options_for_units(self, grade_units, grades_data_map):
		my_units = {}
		for grade in grades_data_map:
			print("{}: ".format(grade), end='')
			unit_index = self.gmanager.get_valid_index(grade_units) - 1
			my_units[grades_data_map[grade]] = unit_index
		return my_units


	def create_block_document(self, mineral_deposit, block_model, amount_headers, headers, grades_data_map, item, weight_column_index, grade_units, my_units):
		document = {"mineral_deposit": mineral_deposit, "block_model": block_model}
		for index in range(amount_headers):
			if headers[index] in grades_data_map.values():
				transformed = self.gmanager.grade_to_percentage(item[index], item[weight_column_index], grade_units[my_units[headers[index]]])
				item[index] = transformed
			document[headers[index]] = item[index]
		return document

	def find_by_coordinates(self, mineral_deposit, block_model, coordinates_string):
		coordinates = [int(x) for x in coordinates_string.strip().split(',')]
		return self.db.blocks.find({ "mineral_deposit_name": mineral_deposit, "block_model": block_model, "x": coordinates[0],"y": coordinates[1],"z": coordinates[2] })

	def get_all_blocks_from_block_model(self, mineral_deposit, block_model):
		return self.db.blocks.find({ "mineral_deposit": mineral_deposit, "block_model": block_model })


	def remove_all_blocks_from_block_model(self, mineral_deposit, block_model):
		return self.db.blocks.remove({ "mineral_deposit_name": mineral_deposit, "block_model": block_model })


	def get_max_x_y_z_value(self, mineral_deposit_name, block_model_name):
		block_model = self.db.block_models.find_one({"mineral_deposit_name": mineral_deposit_name, "name": block_model_name})
		x = block_model["data_map"]["x"]
		y = block_model["data_map"]["y"]
		z = block_model["data_map"]["z"]
		block_max_x = self.db.blocks.find({}).sort([(x, -1)]).limit(1)
		block_max_y = self.db.blocks.find({}).sort([(y, -1)]).limit(1)
		block_max_z = self.db.blocks.find({}).sort([(z, -1)]).limit(1)
		return block_max_x.next()[x], block_max_y.next()[y], block_max_z.next()[z]
