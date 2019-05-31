import pandas as pd

def parse_file(file):
	block_objects = []
	file = open(file, "r")
	raw_data = list(map(lambda row : row.strip().split(), file))
	for element in raw_data:
		try :
			element = list(map(float, element))
		except:
			pass
		block_objects.append(element)
	return block_objects

def parse_file_url(file):
	block_objects = []
	raw_data = list(map(lambda row : row.strip().split(','), file))
	for block in raw_data:
		try :
			block = list(map(float, block))
			block_objects.append(block)
		except:
			pass
	return block_objects

def parse_headers_url(file):
	headers = file.split()
	return headers


def parse_headers(file):
	headers = open(file, "r")
	return headers.readline().strip().split(',')