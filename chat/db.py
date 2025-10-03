"""
Configuración y conexión a MongoDB
"""
from pymongo import MongoClient
from django.conf import settings


def get_mongo_client():
    """
    Retorna el cliente de MongoDB
    """
    client = MongoClient(settings.MONGODB_URI)
    return client


def get_mongo_db():
    """
    Retorna la base de datos de MongoDB
    """
    client = get_mongo_client()
    db = client[settings.MONGODB_DB_NAME]
    return db


def get_conversations_collection():
    """
    Retorna la colección de conversaciones
    """
    db = get_mongo_db()
    collection = db[settings.MONGODB_COLLECTION]
    return collection


def save_conversation(session_id, messages):
    """
    Guarda una conversación en MongoDB
    
    Args:
        session_id (str): ID único de la sesión
        messages (list): Lista de mensajes de la conversación
    """
    collection = get_conversations_collection()
    
    # Actualiza o inserta la conversación
    collection.update_one(
        {'session_id': session_id},
        {
            '$set': {
                'session_id': session_id,
                'messages': messages
            }
        },
        upsert=True
    )
    

def get_conversation(session_id):
    """
    Recupera una conversación de MongoDB
    
    Args:
        session_id (str): ID único de la sesión
        
    Returns:
        dict: Conversación o None si no existe
    """
    collection = get_conversations_collection()
    conversation = collection.find_one({'session_id': session_id})
    return conversation


def test_connection():
    """
    Prueba la conexión a MongoDB
    """
    try:
        client = get_mongo_client()
        # Verifica que podemos listar las bases de datos
        client.server_info()
        print("✅ Conexión exitosa a MongoDB")
        return True
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        return False

