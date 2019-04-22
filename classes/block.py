import json

class Block:
	def __init__(self, model, x, y, z, weight, grade, data):
		self.model = model
		self.x = x
		self.y = y
		self.z = z
		self.weight = weight
		self.grade = grade
		self.data = data

	def __str__(self):
		return "{}\nX: {}\tY: {}\tZ: {}\nWeight: {}\tGrade: {}".format(self.model.upper(), self.x, self.y, self.z, self.weight, self.grade)