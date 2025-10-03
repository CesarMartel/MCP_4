import pymongo
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        if self._client is None:
            try:
                self._client = pymongo.MongoClient(settings.MONGODB_SETTINGS['host'])
                self._db = self._client[settings.MONGODB_SETTINGS['db']]
                logger.info("Conexión a MongoDB establecida exitosamente")
            except Exception as e:
                logger.error(f"Error conectando a MongoDB: {e}")
                raise e
        return self._db
    
    def get_database(self):
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]

# Instancia global para usar en toda la aplicación
mongodb = MongoDBConnection()

