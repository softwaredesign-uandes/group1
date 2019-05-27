from helpers.database_manager import Manager
from helpers.arguments_manager import manage_arguments
from helpers.container import Container


def main(arguments):
	db_manager = Manager()
	manager = Container()
	if args.insert and args.file_input:
		insert(args, db_manager)
	elif args.remove:
		remove(args, db_manager)
	elif args.metrics:
		metrics(args,db_manager, manager)

def insert (args, db_manager):
	if not args.mineral_deposit:
		db_manager.insert_new_mineral_deposit(args.file_input)
	elif not args.block_model:
		db_manager.insert_new_block_model(args.mineral_deposit, args.file_input)
	else:
		db_manager.insert_blocks(args.mineral_deposit, args.block_model, args.file_input)

def remove(args, db_manager):
	db_manager.remove_all_blocks_from_block_model(args.mineral_deposit, args.block_model)

def metrics(args, db_manager, manager):
	if args.mineral_deposit:
		mineral_deposit = db_manager.fetch_mineral_deposit(args.mineral_deposit)
		manager.set_mineral_deposit(mineral_deposit)
		if args.block_model:
			block_model = db_manager.fetch_block_model(args.mineral_deposit, args.block_model)
			blocks = db_manager.get_all_blocks_from_block_model(args.mineral_deposit, args.block_model)
			manager.set_block_model(block_model, blocks)
	manager.interact_with_user()


if __name__ == "__main__":
	ARGS = manage_arguments()
	main(ARGS)
