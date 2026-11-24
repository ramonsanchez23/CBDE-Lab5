from pymongo import MongoClient


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

client.admin.command("ping")

db = client.get_database("test")

collection = db.get_collection("test")

collection.delete_many({})
collection.insert_many([
    {
        'returnflag': 1,
        'linestatus': 1,
        'shipdate': 1,
        'quantity': 1,
        'extendedprice': 1,
        'discount': 0.3,
        'tax': 0.2,
    },
    {
        'returnflag': 1,
        'linestatus': 1,
        'shipdate': 2,
        'quantity': 2,
        'extendedprice': 2,
        'discount': 0.2,
        'tax': 0.2,
    },
    {
        'returnflag': 2,
        'linestatus': 2,
        'shipdate': 3,
        'quantity': 30,
        'extendedprice': 3,
        'discount': 3,
        'tax': 0.1,
    },
    {
        'returnflag': 3,
        'linestatus': 4,
        'shipdate': 1,
        'quantity': 100,
        'extendedprice': 1,
        'discount': 1,
        'tax': 1,
    }
])


result = collection.aggregate([
    { '$match': { 'shipdate': { '$lte': 2 } } },
    { '$group': { 
                    '_id': { 'returnflag': '$returnflag', 'linestatus': '$linestatus' }, 
                    'sum_qty': {'$sum': '$quantity'},
                    'sum_base_price': {'$sum': '$extendedprice'},
                    'sum_disc_price': {'$sum': 
                        {
                            '$multiply': 
                            [
                                '$extendedprice', 
                                {
                                    '$subtract': 
                                    [
                                        1, 
                                        '$discount'
                                    ]
                                }
                            ]
                        }},
                    'sum_charge': {'$sum': 
                        {
                            '$multiply': 
                            [
                                '$extendedprice', 
                                {
                                    '$subtract': 
                                    [
                                        1, 
                                        '$discount'
                                    ]
                                },
                                {
                                    '$add': 
                                    [
                                        1, 
                                        '$tax'
                                    ]
                                }
                            ]
                        }},
                    'avg_qty': {'$avg': '$quantity'},
                    'avg_price': {'$avg': '$extendedprice'},
                    'avg_disc': {'$avg': '$discount'},
                    'count_order': {'$sum': 1},
                }     
    }
])

for item in result:
    print(item)

client.close()
