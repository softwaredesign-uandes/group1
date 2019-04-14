class MineralDeposit:
    def __init__(self, name, minerals, block_models):
        self.name = name
        self.minerals = minerals
        self.block_models = []

    def add_block_model(self, block_model):
    	self.block_models.append(block_model)

    def get_block_model_list(self):
    	return self.block_models
