from classes.block import Block
from itertools import takewhile

class BlockModel:
	def __init__(self, name, mineral_deposit, headers, data_map):
		self.name = name
		self.mineral_deposit = mineral_deposit
		self.headers = headers
		self.data_map = data_map
		self.blocks = []

	def add_blocks(self, block_cursor):
		for element in block_cursor:
			model = element.pop("block_model", None)
			x = element.pop(self.data_map["x"], None)
			y = element.pop(self.data_map["y"], None)
			z = element.pop(self.data_map["z"], None)
			weight = element.pop(self.data_map["weight"], None)
			grade = element.pop(self.data_map["grade"], None)
			new_block = Block(model, x, y, z, weight, grade, element)
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
			total_mineral_weight += block.weight * block.grade
		return total_mineral_weight

	def get_air_percentage(self):
		air_blocks = 0
		for block in self.blocks:
			if block.weight == 0:
				air_blocks += 1
		return air_blocks / self.count_blocks()
