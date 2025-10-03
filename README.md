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

### Requisitos Previos
- Python 3.10 o superior
- MongoDB instalado y ejecutándose localmente (puerto 27017)
- Cuenta de Google Cloud con Vertex AI habilitado
- Credenciales de Google Cloud configuradas

### Instalación

1. **Clonar el repositorio o descargar el proyecto**

2. **Crear y activar un entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar las credenciales de Google Cloud**
   - Asegúrate de tener un proyecto en Google Cloud con Vertex AI habilitado
   - Configura las credenciales de autenticación:
```bash
gcloud auth application-default login
```
   - O establece la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` apuntando a tu archivo de credenciales JSON

5. **Configurar MongoDB**
   - Asegúrate de que MongoDB esté ejecutándose en `localhost:27017`
   - Si usas una configuración diferente, actualiza `MONGODB_URI` en `mongochat/settings.py`

6. **Actualizar el PROJECT_ID en graph.py**
   - Abre `chat/graph.py`
   - Reemplaza `PROJECT_ID = "stone-poetry-473315-a9"` con tu ID de proyecto de Google Cloud

7. **Verificar la configuración (Opcional pero recomendado)**
```bash
python check_setup.py
```
   Este script verificará que todas las dependencias estén instaladas y los servicios configurados correctamente.

8. **Ejecutar las migraciones de Django**
```bash
python manage.py migrate
```

9. **Iniciar el servidor**
```bash
python manage.py runserver
```

10. **Abrir la aplicación**
   - Abre tu navegador en `http://localhost:8000`
   - ¡Comienza a chatear!

### Estructura del Proyecto

```
mongochat/
├── manage.py
├── requirements.txt
├── mongochat/
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # URLs principales
│   └── ...
└── chat/
    ├── templates/
    │   └── chat.html    # Interfaz web del chatbot
    ├── views.py         # Lógica de las vistas
    ├── urls.py          # URLs de la app chat
    ├── graph.py         # Lógica de LangGraph y Vertex AI
    └── db.py            # Funciones de MongoDB
```

### Características Implementadas

✅ Interfaz web moderna y responsive  
✅ Chat en tiempo real con Google Vertex AI (Gemini 2.0)  
✅ Orquestación de conversación con LangGraph  
✅ Persistencia de conversaciones en MongoDB  
✅ Mantenimiento de contexto conversacional  
✅ Gestión de sesiones de usuario  
✅ Botón para limpiar conversaciones  

### Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **IA**: Google Vertex AI (Gemini 2.0 Flash)
- **Orquestación**: LangGraph + LangChain
- **Base de Datos**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

### 🔧 Solución de Problemas

#### Error: "No module named 'X'"
Asegúrate de haber activado el entorno virtual y haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

#### Error de conexión a MongoDB
- Verifica que MongoDB esté ejecutándose: `mongod --version`
- En Windows, inicia el servicio MongoDB desde Servicios
- En Linux/Mac: `sudo systemctl start mongodb` o `brew services start mongodb-community`

#### Error de autenticación de Google Cloud
Ejecuta uno de estos comandos:
```bash
# Opción 1: Autenticación de aplicación por defecto
gcloud auth application-default login

# Opción 2: Descargar credenciales JSON y configurar la variable de entorno
# export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/credenciales.json"
```

#### Error: "TemplateDoesNotExist"
Asegúrate de que la estructura de carpetas sea correcta:
```
chat/
└── templates/
    └── chat.html
```

#### El chatbot no responde
- Verifica que tu proyecto de Google Cloud tenga Vertex AI habilitado
- Confirma que el PROJECT_ID en `chat/graph.py` sea correcto
- Revisa los logs del servidor para ver mensajes de error específicos

### 📚 Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de MongoDB](https://docs.mongodb.com/)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

<img width="1349" height="421" alt="image" src="https://github.com/user-attachments/assets/fd32f5e5-c043-417b-bdb5-28c92233ead8" />
<img width="1120" height="309" alt="image" src="https://github.com/user-attachments/assets/b01100c1-3978-4b30-b99e-c2820f9751e4" />

