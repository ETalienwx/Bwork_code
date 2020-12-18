import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)

db = client.test
collection = db.students

student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

result = collection.insert(student)
print(result)
