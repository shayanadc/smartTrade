import pymongo
import setting
class MongoDB(object):

    def __init__(self,Pair):
        self.myClient = pymongo.MongoClient(setting.MONGOHOST)
        self.db = self.myClient["spot_user_preferences"]
        self.myCol = self.db[Pair]

    def insert(self, input):

        r = self.myCol.insert_one(input)

        return  r.inserted_id

    def findAll(self):
        return self.myCol.find()

    def find(self, query):

        for x in self.myCol.find({}, query):
            return x

    def delete(self, query):

        return self.myCol.delete_many(query)

    def update(self,query,new):

        self.myCol.update_one(query, {'$set': new})