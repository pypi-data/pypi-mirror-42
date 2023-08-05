from bson import ObjectId as BsonObjectId
from smartninja_mongo.environment import is_mongo_env

if is_mongo_env():
    class ObjectId(BsonObjectId):
        pass
else:
    class ObjectId:
        def __new__(cls, *args, **kwargs):
            return str(args[0])
