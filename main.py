from pymongo import MongoClient


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

client.admin.command("ping")

print("Connected successfully")

client.close()
