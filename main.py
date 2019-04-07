import manage_database as manager
from arguments_manager import manage_arguments


def main(args):
	db = manager.get_connection()
	if args.insert:
		if not args.mineral_deposit:
			manager.insert_new_mineral_deposit(db)
		elif not args.block_model:
			manager.insert_new_block_model(db, args.mineral_deposit, args.file_input)
		else:
			manager.insert_blocks(db, args.mineral_deposit, args.block_model, args.file_input)
	elif args.remove:
			manager.remove__all_blocks_from_block_model(db, args.mineral_deposit, args.block_model)
	else:
		block = manager.find_by_coordinates(db, args.mineral_deposit, args.block_model, args.coordinates)
		manager.print_block(block.next())

if __name__ == "__main__":
	args = manage_arguments()
	main(args)
