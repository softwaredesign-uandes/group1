from blocks import Block
import manage_database as manager
from arguments_manager import manage_arguments
from file_parser import parse_file
from bson.json_util import dumps


def main(args):
	db = manager.get_connection()
	if args.insert:
		if not args.block_model:
			manager.insert_new_block_model(db, args.mineral_deposit, args.file_input)
		else:
			block_model = manager.fetch_block_model(db, args.mineral_deposit, args.block_model)
			headers = block_model["fields"]
			data_blocks = parse_file(headers, args.file_input)
			manager.insert_many(db, data_blocks)
	elif args.remove:
			manager.remove_model_blocks(db, args.model)
	else:
		block = manager.find_by_id(db, args.coordinates, args.model)
		manager.print_block(block.next())

if __name__ == "__main__":
	args = manage_arguments()
	main(args)
