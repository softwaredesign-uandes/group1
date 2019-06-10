from pymongo import MongoClient
from connection_params import CONNECTION_PARAMS as params
from file_parser import parse_file, parse_headers, parse_headers_url, parse_file_url
from general_manager import GManager
from bson.objectid import ObjectId

class Manager:
	def __init__(self):
		connection = MongoClient(
	        'mongodb://{user}:{password}@{host}:'
	        '{port}/{namespace}'.format(**params)
	    )
		self.db = connection.mining_blocks
		self.gmanager = GManager()

	def insert_new_mineral_deposit(self, data_file):
		file_of_mineral_deposit_headers = open(data_file)
		data = file_of_mineral_deposit_headers.readline().strip().split(',')
		name = data[0]
		minerals = data[1:]
		self.db.mineral_deposits.insert_one({ "name": name, "minerals": minerals })
	
	def insert_new_mineral_deposit_from_name(self, element):
		self.db.mineral_deposits.insert_one(element)

	def fetch_mineral_deposit(self, mineral_deposit):
		return self.db.mineral_deposits.find_one({ "name": mineral_deposit })

	def fetch_mineral_deposit_by_id(self, mineral_deposit_id):	
		name =  self.db.mineral_deposits.find_one({'_id': ObjectId(mineral_deposit_id)})
		cursor_all_block_models = self.db.block_models.find({'mineral_deposit_name':name['name']})
		return {"id": mineral_deposit_id, "name": name['name'], "block_models": cursor_all_block_models}
	
	def fetch_all_mineral_deposit(self):
		return self.db.mineral_deposits.find({})

	def insert_new_block_model(self, mineral_deposit_name, headers_file):
		headers = parse_headers(headers_file)
		mineral_deposit = self.fetch_mineral_deposit(mineral_deposit_name)
		data_map = self.gmanager.map_headers(headers, mineral_deposit["minerals"])
		name_of_block_model = ""
		while name_of_block_model == "":
			name_of_block_model = input("What would you like to name this block model?\n>>> ")
			if self.fetch_block_model(mineral_deposit_name, name_of_block_model) != None:
				print("A block model with that name already exist within this mineral deposit.")
				name_of_block_model = ""
		self.db.block_models.insert_one({ "name": name_of_block_model, "mineral_deposit_name": mineral_deposit_name, "headers": headers, "data_map": data_map })


	def fetch_block_model(self, mineral_deposit, block_model):
		return self.db.block_models.find_one({ "name": block_model, "mineral_deposit_name": mineral_deposit })

	def fetch_all_block_models(self):
		return self.db.block_models.find()

	def fetch_block_model_from_id(self, block_model_id):
		block_model = self.db.block_models.find_one({'_id': ObjectId(block_model_id)},{'_id':0})
		return block_model

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

	def get_block_from_id(self, block_id):
		return self.db.blocks.find_one({'_id': ObjectId(block_id)},{'_id':0})

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


	##FORAPI##
	def insert_new_block_model_with_name(self, mineral_deposit_name, headers,data_map, name_of_block_model):

		self.db.block_models.insert_one(
			{"name": name_of_block_model, "mineral_deposit_name": mineral_deposit_name, "headers": headers,
			 "data_map": data_map})

	def insert_blocks_from_url(self, mineral_deposit, block_model, data_file, my_units):
		model = self.fetch_block_model(mineral_deposit, block_model)
		headers, amount_headers, data_map, weight_column, weight_column_index, grades_data_map = self.get_params_from_model(model)
		data = parse_file_url(data_file)
		data_array = []
		grade_units = ['tonn', 'percentage', 'oz/tonn', 'ppm']
		for item in data:
			document = self.create_block_document(mineral_deposit,block_model,amount_headers,headers,grades_data_map,item,weight_column_index,grade_units,my_units)
			data_array.append(document)
		self.db.blocks.insert_many(data_array)


