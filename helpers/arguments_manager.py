from argparse import ArgumentParser


def manage_arguments():
	parser = ArgumentParser()

	# Name of the mineral deposit that is to be considered
	mineral_deposit = parser.add_argument_group("mineral_deposit")
	mineral_deposit.add_argument("-md", "--mineral_deposit", help="Name of the mineral deposit that is to be considered")

	# Name of the block model that is to me considered within the context of the provided mineral deposit
	block_model = parser.add_argument_group("block_model")
	block_model.add_argument("-bm", "--block_model", help="Name of the block model that is to me considered within the context of the provided mineral deposit. Leave blank if you are to insert a new block model")
	
	# Action to be exectuted
	action = parser.add_mutually_exclusive_group(required=True)
	action.add_argument("-i", "--insert", help="Indicates that you want to insert data into the database", action="store_true")
	action.add_argument("-s", "--search", help="Indicates that you want to search for specific block within the given block model", action="store_true")
	action.add_argument("-r", "--remove", help="Indicates that you want to remove all blocks belonging to the provided block model", action="store_true")
	action.add_argument("-m", "--metrics", help="Indicates that you want to fetch and analyse data from a given mineral deposit and block model", action="store_true")

	# Directory of the file containing the data to be uploaded to the server
	file_input = parser.add_argument_group("file_input")
	file_input.add_argument("-f", "--file_input", help="Directory of the file containing the data to be uploaded to the server")
	
	# Coordinates X, Y and Z of the desired block to be queried within the given block model
	coordinates = parser.add_argument_group("coordinates")
	coordinates.add_argument("-c", "--coordinates", help="Coordinates X, Y and Z of the desired block, separated only by commas")

	return parser.parse_args()
