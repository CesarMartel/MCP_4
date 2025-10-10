# chat/graph.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from langchain_google_vertexai import ChatVertexAI
import os
import vertexai

# Estado del chat usando TypedDict para mejor compatibilidad
class ChatState(TypedDict):
    messages: list
    reply: str

# Función que llama a Vertex AI
def call_vertex(state: ChatState, config=None, runtime=None):
    print(f"=== DEBUG: call_vertex llamado ===")
    print(f"state: {state}")
    print(f"type(state): {type(state)}")
    print(f"config: {config}")
    print(f"runtime: {runtime}")
    print("=================================")
    
    # Verificar que state no sea None
    if state is None:
        print("ERROR: state es None")
        return {"reply": "[ERROR] Estado del chat no disponible"}
    
    # Obtener mensajes de forma segura
    msgs = state.get("messages", []) if isinstance(state, dict) else []
    
    print(f"=== DEBUG: mensajes extraídos ===")
    print(f"msgs: {msgs}")
    print(f"type(msgs): {type(msgs)}")
    print("=================================")
    
    # Verificar que msgs sea una lista
    if not isinstance(msgs, list):
        print(f"ERROR: msgs no es una lista: {type(msgs)}")
        return {"reply": "[ERROR] Formato de mensajes incorrecto"}
    
    # Configuración del proyecto
    project_id = "stone-poetry-473315-a9"
    location = "us-central1"
    model_name = "gemini-2.0-flash-exp"
    
    # Configurar credenciales
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stone-poetry-473315-a9-e4beaafb3994.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    
    # Inicializar Vertex AI
    try:
        vertexai.init(project=project_id, location=location)
    except Exception as e:
        print(f"Error inicializando Vertex AI: {e}")

    llm = ChatVertexAI(
        model_name=model_name,
        project=project_id,
        location=location,
        temperature=0.2,
        max_output_tokens=512,
    )

    convo_text = "\n".join([f"{m['role']}: {m['text']}" for m in msgs])
    prompt = f"You are a helpful assistant.\nConversation:\n{convo_text}\nAssistant:"

    print("=== PROMPT ENVIADO ===")
    print(prompt)  
    print("======================")

    try:
        response = llm.invoke(prompt)
        print("=== RESPONSE RAW ===")
        print(response)  
        print("===================")
        reply = response.content if hasattr(response, "content") else str(response)
        if not reply.strip():
            reply = "[El modelo no respondió]"
    except Exception as e:
        print("ERROR LLM:", e)
        reply = f"[ERROR LLM] {e}"

    print(f"=== REPLY FINAL ===", reply)
    return {"reply": reply}



# Construcción del grafo
graph_builder = StateGraph(ChatState)
graph_builder.add_node("llm_call", call_vertex)
graph_builder.set_entry_point("llm_call")
graph_builder.add_edge("llm_call", END)

chat_graph = graph_builder.compile()
