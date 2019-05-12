import numpy as np
from classes.abstract_block import AbstractBlock


class Block(AbstractBlock):
	def __init__(self, model, x, y, z, weight, grade_values, data):
		self.model = model
		self.x = x
		self.y = y
		self.z = z
		self.weight = weight
		self.grade_values = grade_values
		self.data = data

	def get_weight(self):
		return self.weight

	def get_grade_values(self):
		return np.array(self.grade_values)

	def __str__(self):
		return "{}\nX: {}\tY: {}\tZ: {}\nWeight: {}\tGrade: {}\t Data: {}".format(
						self.model.upper(), self.x, self.y, self.z, self.weight, self.grade_values, self.data)
