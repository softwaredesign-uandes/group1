from helpers.database_manager import Manager
from helpers.arguments_manager import manage_arguments
from helpers.container import Container


def main(args):
	db_manager = Manager()
	mike = Container()
	if args.insert and args.file_input:
		if not args.mineral_deposit:
			db_manager.insert_new_mineral_deposit(args.file_input)
		elif not args.block_model:
			db_manager.insert_new_block_model(args.mineral_deposit, args.file_input)
		else:
			db_manager.insert_blocks(args.mineral_deposit, args.block_model, args.file_input)
	elif args.remove:
		db_manager.remove__all_blocks_from_block_model(args.mineral_deposit, args.block_model)
	elif args.metrics:
		if args.mineral_deposit:
			mineral_deposit = db_manager.fetch_mineral_deposit(args.mineral_deposit)
			mike.set_mineral_deposit(mineral_deposit)
			if args.block_model:
				block_model = db_manager.fetch_block_model(args.mineral_deposit, args.block_model)
				blocks = db_manager.get_all_blocks_from_block_model(args.mineral_deposit, args.block_model)
				mike.set_block_model(block_model, blocks)
		mike.interact_with_user()
	else:
		block = db_manager.find_by_coordinates(args.mineral_deposit, args.block_model, args.coordinates)
		print(block.next())

if __name__ == "__main__":
	args = manage_arguments()
	main(args)
