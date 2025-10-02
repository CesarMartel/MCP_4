🧠 Reto: Chatbot con Memoria Persistente
Este es un ejercicio práctico para construir una aplicación de IA funcional desde cero. El objetivo es desarrollar un chatbot conversacional con una interfaz web, integrando varias tecnologías de vanguardia.

📝 Descripción del Proyecto
Tu misión es crear una aplicación web que permita a un usuario interactuar con un modelo de lenguaje grande (LLM). La característica principal de este chatbot es su memoria persistente: cada conversación se guardará en una base de datos NoSQL, permitiendo que la aplicación recuerde interacciones pasadas.

Este reto te obligará a pensar en cómo estructurar una aplicación full-stack, gestionar el estado de una conversación y orquestar llamadas a servicios de IA, almacenando los resultados de manera eficiente.

🛠️ Tecnologías Involucradas
Para completar este reto, deberás utilizar y conectar los siguientes componentes:

Backend (Django): Gestionará la lógica del servidor, las peticiones HTTP y renderizará la interfaz de usuario.

Orquestación de IA (LangGraph): Modelará el flujo de la conversación como un grafo de estados.

Inteligencia Artificial (Google Vertex AI): Proveerá el modelo de lenguaje (ej. Gemini) para generar las respuestas.

Base de Datos (MongoDB): Almacenará el historial de cada conversación de forma persistente.

✅ Requisitos Funcionales
La aplicación final debe cumplir con lo siguiente:

Interfaz Web: Una página simple con un campo de texto para enviar mensajes y un área para mostrar el historial de la conversación.

Flujo Conversacional: Al enviar un mensaje, la app debe pasarlo al grafo de LangGraph, que orquestará la llamada al LLM de Google.

Respuesta de la IA: La respuesta generada por el LLM debe mostrarse en la interfaz web, actualizando el chat.

Persistencia de Datos: Cada conversación completa debe ser guardada como un único documento en MongoDB.

🚀 Primeros Pasos
Librerías Necesarias
Asegúrate de tener Python instalado. Luego, puedes guardar las siguientes librerías en un archivo requirements.txt y ejecutar pip install -r requirements.txt.

Plaintext

django
pymongo
langgraph
langchain
langchain-google-vertexai
Estructura de Archivos Sugerida
Para mantener el orden, te recomendamos seguir la estructura estándar de un proyecto Django:

```
mongochat/
├── manage.py
├── mongochat/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── chat/
    ├── templates/
    │   └── chat/
    │       └── chat.html
    ├── views.py
    ├── urls.py
    └── graph.py  <-- Aquí puedes construir tu lógica de LangGraph
```
<img width="1349" height="421" alt="image" src="https://github.com/user-attachments/assets/fd32f5e5-c043-417b-bdb5-28c92233ead8" />
<img width="1120" height="309" alt="image" src="https://github.com/user-attachments/assets/b01100c1-3978-4b30-b99e-c2820f9751e4" />

