#!/usr/bin/env python3
"""
Script para probar la conexión con Vertex AI
"""
import os
import sys
import vertexai
from langchain_google_vertexai import ChatVertexAI

def test_vertex_connection():
    """Prueba la conexión con Vertex AI"""
    
    # Configuración
    project_id = "stone-poetry-473315-a9"
    location = "us-central1"
    model_name = "gemini-2.0-flash-exp"
    
    # Configurar credenciales
    credentials_path = os.path.join(os.path.dirname(__file__), "stone-poetry-473315-a9-e4beaafb3994.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    
    print(f"🔧 Configurando Vertex AI...")
    print(f"   Proyecto: {project_id}")
    print(f"   Ubicación: {location}")
    print(f"   Modelo: {model_name}")
    print(f"   Credenciales: {credentials_path}")
    
    try:
        # Inicializar Vertex AI
        print("\n🚀 Inicializando Vertex AI...")
        vertexai.init(project=project_id, location=location)
        print("✅ Vertex AI inicializado correctamente")
        
        # Crear instancia del modelo
        print("\n🤖 Creando instancia del modelo...")
        llm = ChatVertexAI(
            model_name=model_name,
            project=project_id,
            location=location,
            temperature=0.2,
            max_output_tokens=512,
        )
        print("✅ Modelo creado correctamente")
        
        # Probar una consulta simple
        print("\n💬 Probando consulta...")
        test_prompt = "Hola, ¿cómo estás? Responde brevemente."
        response = llm.invoke(test_prompt)
        
        print(f"📝 Respuesta: {response.content}")
        print("\n🎉 ¡Conexión exitosa con Vertex AI!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 PRUEBA DE CONEXIÓN VERTEX AI")
    print("=" * 50)
    
    success = test_vertex_connection()
    
    if success:
        print("\n✅ Todas las pruebas pasaron correctamente")
        sys.exit(0)
    else:
        print("\n❌ Las pruebas fallaron")
        sys.exit(1)
