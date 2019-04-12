from classes.mineral_deposit import MineralDeposit
from classes.block_model import BlockModel

class  Container:
    def __init__(self):
        self.mineral_deposit = None
        self.block_model = None

    def set_mineral_deposit(self, mineral_deposit):
        self.mineral_deposit = MineralDeposit(mineral_deposit['name'], None)

    def set_block_model(self, block_model, blocks):
        name = block_model['name']
        mineral_deposit = block_model['mineral_deposit_name']
        headers = block_model['headers']
        current_block_model = BlockModel(name, mineral_deposit, headers, blocks)
        self.block_model = current_block_model

