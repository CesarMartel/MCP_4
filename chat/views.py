from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging
from datetime import datetime
from .mongodb import mongodb
from .langgraph_service import chatbot

logger = logging.getLogger(__name__)

class ChatView(View):
    """Vista principal del chat"""
    
    def get(self, request):
        """Muestra la interfaz del chat"""
        return render(request, 'chat/chat.html')

@method_decorator(csrf_exempt, name='dispatch')
class SendMessageView(View):
    """Vista para enviar mensajes al chatbot"""
    
    def post(self, request):
        """Procesa un mensaje del usuario"""
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            user_id = data.get('user_id', 'anonymous')
            
            if not user_message:
                return JsonResponse({
                    'success': False,
                    'error': 'El mensaje no puede estar vacío'
                })
            
            # Obtener historial de conversación desde MongoDB
            conversation_history = self._get_conversation_history(user_id)
            
            # Procesar mensaje con LangGraph
            result = chatbot.process_message(user_message, conversation_history)
            
            if result['success']:
                # Guardar conversación en MongoDB
                self._save_conversation(user_id, result['updated_messages'])
                
                return JsonResponse({
                    'success': True,
                    'bot_response': result['bot_response'],
                    'timestamp': result['timestamp'],
                    'image': result.get('image')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result.get('error', 'Error desconocido')
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Formato JSON inválido'
            })
        except Exception as e:
            logger.error(f"Error en SendMessageView: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor'
            })
    
    def _get_conversation_history(self, user_id):
        """Obtiene el historial de conversación de un usuario desde MongoDB"""
        try:
            collection = mongodb.get_collection('conversations')
            conversation = collection.find_one({'user_id': user_id})
            
            if conversation:
                return conversation.get('messages', [])
            return []
            
        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return []
    
    def _save_conversation(self, user_id, messages):
        """Guarda la conversación en MongoDB"""
        try:
            collection = mongodb.get_collection('conversations')
            
            # Actualizar o crear la conversación
            collection.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'user_id': user_id,
                        'messages': messages,
                        'last_updated': datetime.now().isoformat()
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error guardando conversación: {e}")

@method_decorator(csrf_exempt, name='dispatch')
class GetHistoryView(View):
    """Vista para obtener el historial de conversación"""
    
    def post(self, request):
        """Obtiene el historial de conversación de un usuario"""
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id', 'anonymous')
            
            conversation_history = self._get_conversation_history(user_id)
            
            return JsonResponse({
                'success': True,
                'messages': conversation_history
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Formato JSON inválido'
            })
        except Exception as e:
            logger.error(f"Error en GetHistoryView: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Error interno del servidor'
            })
    
    def _get_conversation_history(self, user_id):
        """Obtiene el historial de conversación de un usuario desde MongoDB"""
        try:
            collection = mongodb.get_collection('conversations')
            conversation = collection.find_one({'user_id': user_id})
            
            if conversation:
                return conversation.get('messages', [])
            return []
            
        except Exception as e:
            logger.error(f"Error obteniendo historial: {e}")
            return []