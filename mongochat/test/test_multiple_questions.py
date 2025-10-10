#!/usr/bin/env python3
"""
Script para probar múltiples preguntas al chatbot
"""
import requests
import json
import time

def test_multiple_questions():
    """Prueba el chatbot con múltiples preguntas"""
    
    url = "http://127.0.0.1:8000/api/chat/"
    questions = [
        "¿Cuál es la capital de Francia?",
        "¿Qué es la inteligencia artificial?",
        "Dime un chiste",
        "¿Cómo se hace un café?"
    ]
    
    print(f"🧪 Probando chatbot con {len(questions)} preguntas...")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Pregunta {i}: {question}")
        
        try:
            response = requests.post(url, data={"message": question})
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('reply', 'No hay respuesta')
                print(f"🤖 Respuesta: {answer}")
                print("-" * 60)
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        # Pequeña pausa entre preguntas
        time.sleep(1)
    
    print("\n🎉 ¡Pruebas completadas!")

if __name__ == "__main__":
    test_multiple_questions()
