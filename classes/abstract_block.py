from abc import ABCMeta, abstractmethod

class AbstractBlock:
	__metaclass__ = ABCMeta

	@classmethod
	def version(cls):
		return "1.0"

	@abstractmethod
	def get_weight(self):
		raise NotImplementedError

	@abstractmethod
	def get_grade_values(self):
		raise NotImplementedError
