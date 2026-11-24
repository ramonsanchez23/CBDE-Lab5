from pymongo import MongoClient


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

client.admin.command("ping")

db = client.get_database("test")

collection = db.get_collection('test')

collection.delete_many({})
collection.insert_many([
    {
        'returnflag': 1,
        'linestatus': 1,
        'shipdate': 1,
        'quantity': 1,
        'extendedprice': 1,
        'discount': 1,
        'tax': 1,
    }
])


result = collection.aggregate([
    { '$match': { 'shipdate': { '$lte': 1 } } },
    { '$group': { '_id': '$returnflag#$linestatus', 'total': { '$sum': '$quantity' } } }
])

for item in result:
    print(item)

client.close()
