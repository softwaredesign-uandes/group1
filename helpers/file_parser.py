def parse_file(file):
	block_objects = []
	file = open(file, "r")
	raw_data = list(map(lambda row : row.strip().split(), file))
	try :
		raw_data = map(float, list(map(lambda row : row.strip().split(), file)))
	except:
		pass
	block_objects.append(raw_data)
	return block_objects


def parse_headers(file):
	headers = open(file, "r")
	return headers.readline().strip().split(',')