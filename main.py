from group1.blocks import Block
from group1 import  manage_database as manager


if __name__ == "__main__":
    db = manager.get_connection()
    print(db.list_collection_names())
