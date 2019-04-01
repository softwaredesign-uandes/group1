from blocks import Block
import manage_database as manager
from arguments_manager import manage_arguments
from file_parser import parse_file
from bson.json_util import dumps


def main(args):
	db = manager.get_connection()
	if args.insert:
		data_blocks = parse_file(args)
		manager.insert_many(db, data_blocks)
	elif args.remove:
			manager.remove_model_blocks(db, "Marvin" if args.marvin else "Zuck small")
	else:
		block = manager.find_by_id(db, args.id, "Marvin" if args.marvin else "Zuck small")
		manager.print_block(block.next())

if __name__ == "__main__":
	args = manage_arguments()
	main(args)
