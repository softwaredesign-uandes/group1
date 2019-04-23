from classes.block import Block
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
		for element in block_cursor[:40]:
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
		result = list(takewhile(lambda block: block.x == x and block.y == y and block.z == z, self.blocks))
		return result[0]

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
		new_total_weight = 0
		new_x = 
		new_y = 
		new_z = 
		for x in range(x_step, x_step + rx):
			for y in range(y_step, y_step + ry):
				for z in range(z_step, z_step + rz):
					new_total_weight += 
		x_step += rx
		y_step += ry
		z_step += rz



		return True