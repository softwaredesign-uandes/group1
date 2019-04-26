def parse_file(file):
	block_objects = []
	file = open(file, "r")
	for row in file:
		raw_data = row.strip().split()
		for index in range(len(raw_data)):
			try:
				float_value = float(raw_data[index])
				raw_data[index] = float_value
			except:
				continue
		block_objects.append(raw_data)
	return block_objects


def parse_headers(file):
	headers = open(file, "r")
	return headers.readline().strip().split(',')