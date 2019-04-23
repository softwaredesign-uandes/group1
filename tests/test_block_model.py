import unittest
from classes.block_model import BlockModel
from unittest.mock import patch

class TestsBlockModel(unittest.TestCase):
    def setUp(self):
        name = "v1"
        mineral_deposit = "Zuck small"
        headers =  ["id", "x", "y", "z", "cost", "value", "rock_tonnes", "ore_tonnes"]
        data_map = {"x": "x", "y": "y", "z": "z", "weight": "rock_tonnes", "grade": {"Au":"ore_tonnes"}}
        self.block_model = BlockModel(name, mineral_deposit, headers, data_map, 19, 25, 0)
        blocks = [{"_id": {"$oid": "5cb0f608b766f9aa245cb3f0"},
                "mineral_deposit": "Zuck small",
                "block_model": "v1",
                "id": 9369,
                "x": 19,
                "y": 25,
                "z": 0,
                "cost": 56592,
                "value": 135786.28,
                "rock_tonnes": 62880,
                "ore_tonnes": 0.25572519083969464
            }, {"_id": {"$oid": "5cb0f608b766f9aa245cb3f1"},
                "mineral_deposit": "Zuck small",
                "block_model": "v1",
                "id": 9370,
                "x": 0,
                "y": 1,
                "z": 0,
                "cost": 56592,
                "value": 115580.184,
                "rock_tonnes": 0,
                "ore_tonnes": 0
                }]
        self.block_model.add_blocks(blocks)

    def test_get_block_by_coordinates(self):
        expected_result = self.block_model.blocks[1]
        block = self.block_model.get_block_by_coordinates(0, 1, 0)
        self.assertEqual(block, expected_result, "The returned block doesn't match the coordinates")

    def test_count_blocks(self):
        number_of_blocks = self.block_model.count_blocks()
        self.assertEqual(number_of_blocks, 2, "Count of blocks does not corresponds to the actual number ")

    def test_get_total_weight(self):
        total_weight = self.block_model.get_total_weight()
        self.assertEqual(total_weight, 62880, "Total weight of blocks is incorrect")

    def test_get_total_mineral_weight(self):
        mineral_weight = self.block_model.get_total_mineral_weight()
        self.assertEqual(mineral_weight, 62880 * 0.25572519083969464 , "Total mineral weight of blocks in block model is incorrect")

    def test_get_air_percentage(self):
        air_percentage = self.block_model.get_air_percentage()
        self.assertEqual(air_percentage, 0.5, "Air percentage of block model is incorrect")

