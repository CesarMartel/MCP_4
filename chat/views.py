from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .graph import conversation_graph
from .db import save_conversation, get_conversation

def chat_view(request):
    """
    Vista principal del chat - Renderiza la interfaz web
    """
    # Generar o recuperar el ID de sesión
    if 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())
    
    session_id = request.session['session_id']
    
    # Recuperar conversación existente o crear una nueva
    conversation = get_conversation(session_id)
    messages = conversation['messages'] if conversation else []
    
    context = {
        'session_id': session_id,
        'messages': messages
    }
    
    return render(request, 'chat.html', context)

@csrf_exempt
def send_message(request):
    """
    Vista para procesar mensajes del usuario y generar respuestas de la IA
    """
    if request.method == 'POST':
        try:
            # Obtener el mensaje del usuario
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id')
            
            if not user_message:
                return JsonResponse({
                    'error': 'El mensaje no puede estar vacío'
                }, status=400)
            
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Recuperar conversación existente
            conversation = get_conversation(session_id)
            messages = conversation['messages'] if conversation else []
            
            # Crear el estado inicial para el grafo
            initial_state = {
                'messages': messages.copy(),
                'user_input': user_message,
                'ai_response': ''
            }
            
            # Ejecutar el grafo de conversación
            result = conversation_graph.invoke(initial_state)
            
            # Guardar la conversación actualizada en MongoDB
            save_conversation(session_id, result['messages'])
            
            # Retornar la respuesta
            return JsonResponse({
                'success': True,
                'message': result['ai_response'],
                'session_id': session_id,
                'all_messages': result['messages']
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Error al procesar el mensaje: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'error': 'Método no permitido'
    }, status=405)

def clear_conversation(request):
    """
    Vista para limpiar la conversación actual
    """
    if request.method == 'POST':
        # Generar un nuevo ID de sesión
        request.session['session_id'] = str(uuid.uuid4())
        
        return JsonResponse({
            'success': True,
            'message': 'Conversación reiniciada',
            'session_id': request.session['session_id']
        })
    
    return JsonResponse({
        'error': 'Método no permitido'
    }, status=405)
