# MongoChat - Chatbot con IA

Un chatbot web moderno construido con Django, React, MongoDB y Vertex AI (Gemini).

## 🚀 Características

### Backend (Django)
- **API REST** para comunicación con el frontend
- **Integración con Vertex AI** usando Gemini 2.0 Flash
- **LangGraph** para controlar el flujo de conversación
- **MongoDB** para persistir las conversaciones

### Frontend (React)
- **Interfaz** con gradientes y animaciones
- **Panel de historial** con conversaciones guardadas
- **Responsive design** para móviles y escritorio
- **Botón de nuevo chat** para iniciar conversaciones
- **Datos de ejemplo** para demostración

## 🛠️ Tecnologías

### Backend
- Django 5.2.7
- Python 3.13
- MongoDB (PyMongo)
- LangChain + LangGraph
- Google Vertex AI (Gemini)
- django-cors-headers

### Frontend
- React 18
- Vite
- Lucide React (iconos)
- CSS moderno con gradientes

## 📁 Estructura del Proyecto

mongochat/
├── backend/                 # Django backend
│   ├── chat/               # App principal
│   │   ├── graph.py        # LangGraph + Vertex AI
│   │   ├── views.py        # API endpoints
│   │   └── models.py       # Modelos de datos
│   ├── mongochat/          # Configuración Django
│   └── requirements.txt    # Dependencias Python
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── utils/          # Utilidades
│   │   └── App.jsx         # Componente principal
│   └── package.json        # Dependencias Node.js
└── README.md

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
git clone <tu-repositorio>
cd mongochat

### 2. Configurar el Backend (Django)

#### Activar entorno virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

#### Instalar dependencias
pip install -r requirements.txt

#### Configurar credenciales de Google Cloud
1. Coloca tu archivo de credenciales JSON en la raíz del proyecto
2. Asegúrate de que el `project_id` en `chat/graph.py` coincida con tu proyecto

#### Ejecutar migraciones
python manage.py migrate

#### Iniciar servidor Django
python manage.py runserver

### 3. Configurar el Frontend (React)

#### Navegar al directorio frontend
cd frontend

#### Instalar dependencias
npm install

#### Iniciar servidor de desarrollo
npm run dev

### 4. Acceder a la aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/chat/

## 🔧 Configuración Avanzada

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Google Cloud Vertex AI
VERTEX_PROJECT_ID=tu-proyecto-id
VERTEX_LOCATION=us-central1
VERTEX_MODEL_NAME=gemini-2.0-flash-exp
GOOGLE_APPLICATION_CREDENTIALS=ruta-a-tu-archivo-json

# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=mongochat_db

### Error de conexión a MongoDB
- Asegúrate de que MongoDB esté ejecutándose
- Verifica la URI de conexión