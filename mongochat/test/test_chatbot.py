#!/usr/bin/env python3
"""
Script para probar el chatbot directamente
"""
import requests
import json

def test_chatbot():
    """Prueba el chatbot enviando un mensaje"""
    
    url = "http://127.0.0.1:8000/api/chat/"
    test_message = "dime 2 marcas de laptop"
    
    print(f"🧪 Probando chatbot...")
    print(f"   URL: {url}")
    print(f"   Mensaje: {test_message}")
    
    try:
        # Enviar POST request
        response = requests.post(url, data={"message": test_message})
        
        print(f"\n📊 Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Respuesta: {data.get('reply', 'No hay respuesta')}")
            print("\n✅ ¡Chatbot funcionando correctamente!")
            return True
        else:
            print(f"   Error: {response.text}")
            print("\n❌ Error en el servidor")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ No se pudo conectar al servidor. ¿Está Django ejecutándose?")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 PRUEBA DEL CHATBOT")
    print("=" * 50)
    
    success = test_chatbot()
    
    if success:
        print("\n🎉 ¡Prueba exitosa!")
    else:
        print("\n💥 Prueba fallida")
