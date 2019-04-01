from blocks import Block


def parse_file(args):
	block_objects = []
	file = open(args.file, "r")
	if args.zuck_small:
		return parse_zuck_small(file)
	else:
		return parse_marvin(file)


def parse_zuck_small(file):
	block_objects = []
	for row in file:
		raw_data = row.strip().split()
		format_data = list(map(int, raw_data[:4]))
		zs_data = list(map(float, raw_data[4:]))
		weight, grade = zs_data[2], zs_data[3]
		format_data += [weight, grade]
		block_objects.append(Block('Zuck small', format_data[0], format_data[1], format_data[2], format_data[3], format_data[4], format_data[5]).as_json())
	return block_objects


def parse_marvin(file):
	block_objects = []
	for row in file:
		raw_data = row.strip().split()
		format_data = list(map(int, raw_data[:4]))
		m_data = list(map(float, raw_data[4:]))
		weight, grade = m_data[0], m_data[2]
		format_data += [weight, grade]
		block_objects.append(Block('Marvin', format_data[0], format_data[1], format_data[2], format_data[3], format_data[4], format_data[5]).as_json())
	return block_objects