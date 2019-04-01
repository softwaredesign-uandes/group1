from blocks import Block
import manage_database as manager
from arguments_manager import manage_arguments
from file_parser import parse_file
from bson.json_util import dumps


def main(args):
	db = manager.get_connection()
	# print(db.list_collection_names())
	if args.insert:
		# data_blocks would be an array that is to be traveled and each element should be loaded to the database
		data_blocks = parse_file(args)
		for block in data_blocks:
			manager.insert_one_block(db, block)
	else:
		if args.marvin:
			block = manager.find_by_id(db, args.id, "Marvin")
			manager.print_block(block.next())
		else:
			block = manager.find_by_id(db, args.id, "Zuck small")
			manager.print_block(block.next())
		# here you should fetch the block from the database that has this id

if __name__ == "__main__":
	args = manage_arguments()
	main(args)
