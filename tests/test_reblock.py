import unittest
from classes.block_model import BlockModel


class TestReblock(unittest.TestCase):
	def setUp(self):
		name = "v1"
		mineral_deposit = "Zuck small"
		headers =  ["id", "x", "y", "z", "cost", "value", "rock_tonnes", "ore_tonnes"]
		data_map = {"x": "x", "y": "y", "z": "z", "weight": "rock_tonnes", "grade": {"Au":"ore_tonnes"}}
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
				"x": 20,
				"y": 25,
 				"z": 0,
				"cost": 56592,
				"value": 115580.184,
				"rock_tonnes": 0,
                "ore_tonnes": 0	}]

	def test_reblock(self):
		self.assertEqual(BlockModel.reblock(rx, ry, rz), True)