import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:<password>@cluster0.dodrtm6.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)


