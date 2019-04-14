import unittest
from classes.block_model import BlockModel

class TestsBlockModel(unittest.TestCase):
    def setUp(self):
        name = "v1"
        mineral_deposit = "Zuck small"
        headers =  ["id", "x" , "y", "z", "cost", "value", "rock_tonnes", "ore_tonnes"]
        data_map = {"x": "x","y": "y","z": "z","weight": "rock_tonnes","grade": "ore_tonnes"}
        self.block_model = BlockModel(name, mineral_deposit, headers, data_map)

        blocks = [{"_id": {
                "$oid": "5cb0f608b766f9aa245cb3f0"},"mineral_deposit": "Zuck small","block_model": "v1",
                "id": 9369,
                "x": 19,
                "y": 25,
                "z": 0,
                "cost": 56592,
                "value": 135786.28,
                "rock_tonnes": 62880,
                "ore_tonnes": 0.25572519083969464
        }]
        self.block_model.add_blocks(blocks)



    def test_count_blocks(self):
        number_of_blocks = self.block_model.count_blocks()
        self.assertEquals(number_of_blocks, 1, "Count of blocks does not corresponds to the actual number ")

    