from argparse import ArgumentParser


def manage_arguments():
	parser = ArgumentParser()
	action = parser.add_mutually_exclusive_group(required=True)
	action.add_argument("-i", "--insert", help="indicates that you want to insert data into the database", action="store_true")
	action.add_argument("-s", "--search", help="indicates that you want to search for a block", action="store_true")
	action.add_argument("-r", "--remove", help="indicates that you want to remove all blocks from a certain model", action="store_true")
	instance = parser.add_mutually_exclusive_group(required=True)
	instance.add_argument("-m", "--marvin", help="indicates that you are about to enter data from marvin instance", action="store_true")
	instance.add_argument("-zs", "--zuck_small", help="indicates that you are about to enter data from zuck_small instance", action="store_true")
	file_input = parser.add_argument_group("file_input")
	file_input.add_argument("-f", "--file", help="indicates that you are about to enter the data file directory")
	id = parser.add_argument_group("id")
	id.add_argument("-id", "--id", help="id integer of the desired block", type=int)
	return parser.parse_args()