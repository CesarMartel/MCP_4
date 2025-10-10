from django.shortcuts import render
from django.http import JsonResponse
from chat.graph import chat_graph, ChatState
from pymongo import MongoClient
import os
from datetime import datetime

# Conexión a MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB", "mongochat_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
conversations = db["conversaciones"]  # tu colección

# Vista principal del chat
def chat_page(request):
    return render(request, "chat/chat.html")

# API para enviar/recibir mensajes
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Para evitar problemas con CSRF en desarrollo
def chat_api(request):
    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        if not user_msg:
            return JsonResponse({"reply": "[ERROR] Mensaje vacío"}, status=400)

        # Crear estado inicial
        state = ChatState(messages=[{"role": "user", "text": user_msg}])

        try:
            # Ejecutar grafo de Vertex AI
            result = chat_graph.invoke(state)
            
            if result is None:
                reply = "[ERROR] El grafo no devolvió resultado"
            elif isinstance(result, dict):
                reply = result.get("reply", "[ERROR] No se recibió respuesta")
            else:
                reply = f"[ERROR] Formato de resultado inesperado: {type(result)}"
                
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"=== ERROR DETALLADO ===")
            print(error_details)
            print("=======================")
            reply = f"[ERROR INTERNO] {e}"

        # Guardar conversación en MongoDB
        conversations.insert_one({
            "timestamp": datetime.utcnow(),
            "user_message": user_msg,
            "bot_reply": reply
        })

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Método no permitido"}, status=405)
