from helpers.database_manager import Manager
from helpers.arguments_manager import manage_arguments
from helpers.container import Container


def main(arguments):
	db_manager = Manager()
	manager = Container()
	if arguments.insert and arguments.file_input:
		if not arguments.mineral_deposit:
			db_manager.insert_new_mineral_deposit(arguments.file_input)
		elif not arguments.block_model:
			db_manager.insert_new_block_model(arguments.mineral_deposit, arguments.file_input)
		else:
			db_manager.insert_blocks(arguments.mineral_deposit, arguments.block_model, arguments.file_input)
	elif arguments.remove:
		db_manager.remove_all_blocks_from_block_model(arguments.mineral_deposit, arguments.block_model)
	elif arguments.metrics:
		if arguments.mineral_deposit:
			mineral_deposit = db_manager.fetch_mineral_deposit(arguments.mineral_deposit)
			manager.set_mineral_deposit(mineral_deposit)
			if arguments.block_model:
				block_model = db_manager.fetch_block_model(arguments.mineral_deposit, arguments.block_model)
				blocks = db_manager.get_all_blocks_from_block_model(
								arguments.mineral_deposit, arguments.block_model)
				manager.set_block_model(block_model, blocks)
		manager.interact_with_user()

if __name__ == "__main__":
	ARGS = manage_arguments()
	main(ARGS)
