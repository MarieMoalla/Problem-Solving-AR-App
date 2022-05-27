# -*- coding: utf-8 -*-
import pymongo

uri = "mongodb://mariemmoalla:gu6fNXtrD0mHI7kC8UtSRAJkmj8Tvp6u52EwCTTg2oI1zHLxPpCh2zuXQz95fLphrELmaUJavSNqjnfX2wlY3w==@mariemmoalla.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mariemmoalla@"
client = pymongo.MongoClient(uri)
db_connection = client["ProblemSolvingAR"]
collection = db_connection["teams"]


