from classes.block import Block

class BlockModel:
	def __init__(self, name, mineral_deposit, headers, data_map):
		self.name = name
		self.mineral_deposit = mineral_deposit
		self.headers = headers
		self.data_map = data_map
		self.blocks = []

	def add_blocks(self, block_cursor):
		for element in block_cursor:
			keys = list(element.keys())
			model = element.pop("block_model", None)
			x = element.pop(keys[self.data_map["x"]], None)
			y = element.pop(keys[self.data_map["y"]], None)
			z = element.pop(keys[self.data_map["z"]], None)
			weight = element.pop(keys[self.data_map["weight"]], None)
			grade = element.pop(keys[self.data_map["grade"]], None)
			new_block = Block(model, x, y, z, weight, grade, element)
			self.blocks.append(new_block)

	def count_blocks(self):
		return len(self.blocks)

	def get_total_weight(self):
		total_weight = 0.0
		for block in self.blocks:
			total_weight += block.weight
		return total_weight

