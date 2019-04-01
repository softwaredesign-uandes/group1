import json

class Block:
	def __init__(self, model, id, x, y, z, weight, grade):
		self.model = model
		self.id = id
		self.x = x
		self.y = y
		self.z = z
		self.weight = weight
		self.grade = grade

	def as_json(self):
		data = {
		'model': self.model,
		'id': self.id,
		'x': self.x,
		'y': self.y,
		'z': self.z,
		'weight': self.weight,
		'grade': self.grade,
		}
		return json.dumps(data)

	def __str__(self):
		return "{} (id: {})\nX: {}\tY: {}\tZ: {}\nWeight: {}\tGrade: {}".format(self.model.upper(), self.id, self.x, self.y, self.z, self.weight, self.grade)
