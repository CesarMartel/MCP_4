import vertexai
from vertexai.generative_models import GenerativeModel
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_google_vertexai import ChatVertexAI

PROJECT_ID = "stone-poetry-473315-a9"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Definición del estado del grafo
class ConversationState(TypedDict):
    """
    Estado de la conversación que se pasa entre nodos del grafo
    """
    messages: list  # Historial de mensajes
    user_input: str  # Último mensaje del usuario
    ai_response: str  # Respuesta generada por la IA

def process_user_input(state: ConversationState) -> ConversationState:
    """
    Nodo que procesa la entrada del usuario
    """
    user_message = {
        "role": "user",
        "content": state["user_input"]
    }
    
    # Añadir el mensaje del usuario al historial
    state["messages"].append(user_message)
    
    return state

def generate_ai_response(state: ConversationState) -> ConversationState:
    """
    Nodo que genera la respuesta de la IA usando Vertex AI
    """
    try:
        # Inicializar el modelo con LangChain
        model = ChatVertexAI(
            model_name="gemini-2.0-flash-exp",
            project=PROJECT_ID,
            location=LOCATION
        )
        
        # Construir el prompt con el historial
        conversation_history = ""
        for msg in state["messages"]:
            role = "Usuario" if msg["role"] == "user" else "Asistente"
            conversation_history += f"{role}: {msg['content']}\n"
        
        # Generar respuesta
        prompt = f"""Eres un asistente conversacional útil y amigable.
        
Historial de la conversación:
{conversation_history}

Por favor, responde al último mensaje del usuario de manera natural y útil."""
        
        response = model.invoke(prompt)
        ai_message_content = response.content
        
        # Añadir la respuesta al historial
        ai_message = {
            "role": "assistant",
            "content": ai_message_content
        }
        state["messages"].append(ai_message)
        state["ai_response"] = ai_message_content
        
    except Exception as e:
        error_message = f"Error al generar respuesta: {str(e)}"
        state["ai_response"] = error_message
        state["messages"].append({
            "role": "assistant",
            "content": error_message
        })
    
    return state

def create_conversation_graph():
    """
    Crea y compila el grafo de conversación
    """
    # Crear el grafo
    workflow = StateGraph(ConversationState)
    
    # Añadir nodos
    workflow.add_node("process_input", process_user_input)
    workflow.add_node("generate_response", generate_ai_response)
    
    # Definir el flujo
    workflow.set_entry_point("process_input")
    workflow.add_edge("process_input", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Compilar el grafo
    app = workflow.compile()
    
    return app

# Crear la instancia del grafo
conversation_graph = create_conversation_graph()