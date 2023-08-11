import pymongo,os
from dotenv import load_dotenv

load_dotenv()
MONGODB = os.environ.get("MONGODB")

class MongoDB:
    # class for Mongodb
    def __init__(self) -> None:
        self.URL = MONGODB
        self.dbname = "GuessDice" # replace with your own database name in mongodb
        self.coll = "users" # replace with your own collection name in mongodb

class User:
    # class for user
    def __init__(self,m = None) -> None:
        self.id          : int
        self.first_name  : str
        self.last_name   : str
        self.username    : str 
        
        if m != None: # m holds the user data from the telebot
            self.id         = m.from_user.id
            self.first_name = m.from_user.first_name
            self.last_name  = m.from_user.last_name
            self.username   = m.from_user.username

class Players:
    # class for all Players
    def __init__(self) -> None:
        self.db = MongoDB()
        self.users = {}
        self.load_users() # load all users

    def getCollection(self,db:pymongo.MongoClient):
        return db[self.db.dbname][self.db.coll]  # return the collection in mongodb to perform read/write operations.

    def getLead(self):
        with pymongo.MongoClient(self.db.URL) as db:
            database = db[self.db.dbname]
            coll = database[self.db.coll]
            return [i for i in coll.find().sort('score',-1).limit(5)] # returns top 5 score 
            
    def load_users(self):
        with pymongo.MongoClient(self.db.URL) as db:
            coll = self.getCollection(db)
            for i in coll.find():
                self.users.update({i['_id']:i}) 

    def get_userscore(self,user:User): # method to get specific user's score
        id = user.id
        with pymongo.MongoClient(self.db.URL) as db:
            coll = self.getCollection(db)
            score = coll.find_one({'_id':id})
            update = {'_id':id,
                            'score':0,
                            'first_name':user.first_name,
                            'second_name':user.last_name,
                            'username':user.username
                        }
            if score == None :
                coll.insert_one(update)
                self.users.update({user.id:update})
                return 0
            else : 
                update['score'] = score['score']
                self.users.update({user.id:update});
                return score["score"]

    def set_score(self,user:User,score): # method to set specific score with specific user
        id = user.id
        with pymongo.MongoClient(self.db.URL) as db:
            coll = self.getCollection(db)
            update = {
                    '_id':id,
                    'score':score,
                    'first_name':user.first_name,
                    'second_name':user.last_name,
                    'username':user.username
                    }
            try:
                coll.update_one({'_id':id},{"$set":update})
            except :
                coll.insert_one(update)
            self.users.update({user.id:update})

    def increament(self,id,val=1): # add 1 to the existing score of the user
        score = self.get_userscore(id)
        self.set_score(id,score+val)

    def decreament(self,id,val=1): # decrease 1 to the existing score of the user
        self.increament(id,val*-1)
