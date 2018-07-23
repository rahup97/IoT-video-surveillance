from pymongo import MongoClient

client = MongoClient()
db = client.home_surveillance

def insert_entry_time(id_, entry_time):
    db.times.insert({"motion_id":id_, "Entry":entry_time})

def insert_exit_time(id_, exit_time):
    db.times.insert({"motion_id":id_, "Exit":exit_time})
