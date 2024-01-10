import datetime
import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pymongo:password@cluster0.dodrtm6.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)

# definição de info para compor o doc
post = {
    "author": "Mike",
    "text": "My first mongodb application based on python",
    "tags": ["mongodb","python3", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.posts)