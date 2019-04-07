def parse_file(headers, file):
	block_objects = []
	file = open(file, "r")
	for row in file:
		raw_data = row.strip().split()
		indicators = [int(x) for x in raw_data[:4]]
		tail = [float(x) for x in raw_data[4:]]
		block_objects.append(indicators + tail)
	return block_objects


def parse_headers(file):
	headers = open(file, "r")
	return headers.readline().strip().split(',')