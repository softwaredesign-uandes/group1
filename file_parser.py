from blocks import Block


def parse_file(headers, file):
	block_objects = []
	file = open(file, "r")
	for row in file:
		raw_data = row.strip().split()