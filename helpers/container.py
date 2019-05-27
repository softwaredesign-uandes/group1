from classes.mineral_deposit import MineralDeposit
from classes.block_model import BlockModel
from .database_manager import Manager

class  Container:
    def __init__(self):
        self.mineral_deposit = None
        self.block_model = None
        self.db_manager = Manager()

    def set_mineral_deposit(self, mineral_deposit):
        self.mineral_deposit = MineralDeposit(mineral_deposit['name'], None)

    def set_block_model(self, block_model, blocks):
        name = block_model['name']
        mineral_deposit = block_model['mineral_deposit_name']
        headers = block_model['headers']
        data_map = block_model['data_map']
        max_x, max_y, max_z = self.db_manager.get_max_x_y_z_value(mineral_deposit, name)
        self.block_model = BlockModel(name, mineral_deposit, headers, data_map, max_x, max_y, max_z)
        self.block_model.add_blocks(blocks)

    def interact_with_user(self):
        # self.present_self()
        metrics = ['Search by coordinates', 'Number of blocks', 'Total weight of the mineral deposit', 'Total mineral weight of the mineral deposit', 'Percentage of "Air" blocks']
        print("Choose a metric: ")
        for index in range(len(metrics)):
            print("\t{}: {}".format(index + 1, metrics[index]))
        response = int(input("\t")) - 1
        if metrics[response] == "Search by coordinates":
            print(self.get_block_by_coordinates())
        elif metrics[response] == "Number of blocks":
            print("This block model has {} blocks in it.".format(self.get_number_of_blocks()))
        elif metrics[response] == 'Total weight of the mineral deposit':
            print("The total weight of {} is {}.".format(self.mineral_deposit.name, self.get_total_weight_of_mineral_deposit()))
        elif metrics[response] == 'Total mineral weight of the mineral deposit':
            print("The total mineral weight of {} is {}.".format(self.mineral_deposit.name, self.get_total_mineral_weight_of_mineral_deposit()))
        elif metrics[response] == 'Percentage of "Air" blocks':
            print("The air blocks percentage of {} is {}.".format(self.mineral_deposit.name, self.get_air_blocks_percentage_of_mineral_deposit()))

    def present_to_user_the_options(self):
        print("Welcome to the mining block monitor system.")
        if self.mineral_deposit is None:
            db_manager = Manager()
            mineral_deposit_name = input("It seems that you didn't provide a mineral deposit name.\nPlease indicate the name of the one would you like to use: ")
            db_result = db_manager.fetch_mineral_deposit(mineral_deposit_name)
            self.set_mineral_deposit(db_result)

    def get_block_by_coordinates(self):
        return self.block_model.get_block_by_coordinates()

    def get_number_of_blocks(self):
        return self.block_model.count_blocks()

    def get_total_weight_of_mineral_deposit(self):
        return self.block_model.get_total_weight()

    def get_total_mineral_weight_of_mineral_deposit(self):
        return self.block_model.get_total_mineral_weight()

    def get_air_blocks_percentage_of_mineral_deposit(self):
        return self.block_model.get_air_percentage()

