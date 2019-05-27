import numpy as np
from classes.abstract_block import AbstractBlock


class BlockGroup(AbstractBlock):
	def __init__(self, model, x, y, z):
		self.model = model
		self.x = x
		self.y = y
		self.z = z
		self.blocks = []

	def add_block(self, block):
		self.blocks.append(block)

	def get_weight(self):
		total_weight = 0
		for block in self.blocks:
			total_weight += block.get_weight()
		return total_weight

	def get_grade_values(self):
		total_grade_values = np.array(self.blocks[0].get_grade_values())
		for block in self.blocks[1:]:
			total_grade_values += np.array(block.get_grade_values())
		return total_grade_values
