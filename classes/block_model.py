from classes.block import Block
import numpy as np
from itertools import takewhile

class BlockModel:
	def __init__(self, name, mineral_deposit, headers, data_map, max_x, max_y, max_z):
		self.name = name
		self.mineral_deposit = mineral_deposit
		self.headers = headers
		self.data_map = data_map
		self.blocks = []
		self.max_x = max_x
		self.max_y = max_y
		self.max_z = max_z

	def add_blocks(self, block_cursor):
		for element in block_cursor:
			model = element.pop("block_model", None)
			x = element.pop(self.data_map["x"], None)
			y = element.pop(self.data_map["y"], None)
			z = element.pop(self.data_map["z"], None)
			weight = element.pop(self.data_map["weight"], None)
			grades =self.data_map["grade"].values()
			grades_values = []
			for grade in grades:
				mineral_grade = element.pop(grade, None)
				grades_values.append(mineral_grade)
			new_block = Block(model, x, y, z, weight, grades_values, element)
			self.blocks.append(new_block)

	def get_block_by_coordinates(self,x, y, z):
		result = next((block for block in self.blocks if block.x == x and block.y == y and block.z == z), None)
		return result

	def count_blocks(self):
		return len(self.blocks)

	def get_total_weight(self):
		total_weight = 0.0
		for block in self.blocks:
			total_weight += block.weight
		return total_weight

	def get_total_mineral_weight(self):
		total_mineral_weight = 0
		for block in self.blocks:
			for grade in block.grade_values:
				total_mineral_weight += block.weight * grade
		return total_mineral_weight

	def get_air_percentage(self):
		air_blocks = 0
		for block in self.blocks:
			if block.weight == 0:
				air_blocks += 1
		return air_blocks / self.count_blocks()

	def reblock(self, rx, ry, rz):
		new_blocks = []
		amount_blocks = rx * ry * rz
		x_step, y_step, z_step = 0, 0, 0
		new_x, new_y, new_z = 0, 0, 0
		for old_x in range(0, self.max_x+1, rx):
			for old_y in range(0, self.max_y+1, ry):
				for old_z in range(0, self.max_z+1, rz):
					new_data = self.get_block_by_coordinates(old_x, old_y, old_z).data
					new_total_weight = 0
					new_grade_values = np.zeros(len(self.data_map['grade']))
					for x in range(old_x, min(old_x + rx, self.max_x+1)):
						for y in range(old_y, min(old_y + ry, self.max_y+1)):
							for z in range(old_z, min(old_z + rz, self.max_z+1)):
								#print( x, y, z)
								current_block = self.get_block_by_coordinates(x, y, z)
								new_total_weight += current_block.weight
								new_grade_values += (np.array(current_block.grade_values) * current_block.weight)
					if new_total_weight!=0:
						new_grade_values /= new_total_weight
					self.set_new_max_coordinates(new_x, new_y, new_z)
					new_blocks.append(Block(self.name, new_x, new_y, new_z, new_total_weight, new_grade_values, new_data))
					new_z +=1
				new_y += 1
			new_x += 1
		self.blocks = new_blocks



		return True

	def set_new_max_coordinates(self, new_x, new_y, new_z):
		self.max_x = new_x
		self.max_y = new_y
		self.max_z = new_z