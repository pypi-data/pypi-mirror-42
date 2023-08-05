from tinydb_serialization import SerializationMiddleware
from tinymongo.serializers import DateTimeSerializer
from smartninja_mongo.environment import is_mongo_env

if is_mongo_env():
    from pymongo import MongoClient as RealMongoClient

    class MongoClient(RealMongoClient):
        pass
else:
    from tinymongo import TinyMongoClient

    class MongoClient(TinyMongoClient):
        def __init__(self, host=None, port=None, document_class=dict, tz_aware=None, connect=None, **kwargs):
            if not host or "://" in host:  # if it's URL
                host = "localhost.db"

            super().__init__(foldername=host)

        @property
        def _storage(self):
            serialization = SerializationMiddleware()
            serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
            # register other custom serializers
            return serialization
