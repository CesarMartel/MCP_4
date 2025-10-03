# Chatbot con Django, LangGraph y Google Vertex AI

Un chatbot inteligente que utiliza Django como backend, LangGraph para modelar el flujo conversacional, Google Vertex AI (Gemini) para generar respuestas y MongoDB para almacenar el historial de conversaciones.

## 🚀 Características

- **Backend Django**: Manejo de rutas, vistas y plantillas
- **LangGraph**: Modelado del flujo conversacional como un grafo de estados
- **Google Vertex AI**: Integración con Gemini para generar respuestas inteligentes
- **MongoDB**: Almacenamiento persistente del historial de conversaciones
- **Interfaz Web**: Chat moderno y responsivo con Bootstrap
- **Memoria Persistente**: Las conversaciones se guardan y recuperan automáticamente

## 📋 Requisitos Previos

- Python 3.8+
- MongoDB (local o en la nube)
- Cuenta de Google Cloud Platform con Vertex AI habilitado
- Credenciales de servicio de Google Cloud

## 🛠️ Instalación y Configuración Completa

### Paso 1: Preparar el Entorno de Desarrollo

#### 1.1 Verificar Python
```bash
# Verificar que tienes Python 3.8 o superior
python --version
# o
python3 --version
```

#### 1.2 Crear entorno virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv chatbot_env

# Activar entorno virtual
# En Windows:
chatbot_env\Scripts\activate
# En Linux/Mac:
source chatbot_env/bin/activate
```

#### 1.3 Actualizar pip
```bash
pip install --upgrade pip
```

### Paso 2: Instalar Dependencias

```bash
# Navegar al directorio del proyecto
cd chatbot_funcional

# Instalar las dependencias
pip install -r requirements.txt
```

### Paso 3: Configurar MongoDB

#### 3.1 Opción A: MongoDB Local
```bash
# Instalar MongoDB (si no lo tienes)
# En Windows: Descargar desde https://www.mongodb.com/try/download/community
# En Ubuntu/Debian:
sudo apt-get install mongodb
# En macOS con Homebrew:
brew install mongodb-community

# Iniciar MongoDB
# En Windows: mongod
# En Linux/Mac: sudo systemctl start mongod
```

#### 3.2 Opción B: MongoDB Atlas (Recomendado para desarrollo)
1. Ve a [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crea una cuenta gratuita
3. Crea un nuevo cluster
4. Obtén la cadena de conexión

### Paso 4: Configurar Google Cloud Platform

#### 4.1 Crear Proyecto en Google Cloud
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Anota el ID del proyecto

#### 4.2 Habilitar APIs necesarias
1. En la consola, ve a "APIs y servicios" > "Biblioteca"
2. Busca y habilita:
   - **Vertex AI API**
   - **AI Platform API**

#### 4.3 Crear cuenta de servicio
1. Ve a "IAM y administración" > "Cuentas de servicio"
2. Haz clic en "Crear cuenta de servicio"
3. Nombre: `chatbot-service`
4. Descripción: `Servicio para el chatbot con Vertex AI`
5. Haz clic en "Crear y continuar"

#### 4.4 Asignar permisos
1. En "Otorgar acceso a esta cuenta de servicio", selecciona:
   - **Vertex AI User**
   - **AI Platform Developer**
2. Haz clic en "Continuar" y luego "Listo"

#### 4.5 Descargar credenciales
1. En la lista de cuentas de servicio, haz clic en la que creaste
2. Ve a la pestaña "Claves"
3. Haz clic en "Agregar clave" > "Crear nueva clave"
4. Selecciona "JSON" y descarga el archivo
5. **Guarda este archivo en una ubicación segura**

### Paso 5: Configurar Variables de Entorno

#### 5.1 Crear archivo .env
```bash
# En la raíz del proyecto, crear archivo .env
touch .env
```

#### 5.2 Configurar variables
Copia el contenido de `env_example.txt` y modifica según tu configuración:

```env
# MongoDB Configuration
# Para MongoDB local:
MONGODB_HOST=mongodb://localhost:27017/
# Para MongoDB Atlas, usa tu cadena de conexión:
# MONGODB_HOST=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB=chatbot_db

# Google Cloud Configuration
# Ruta al archivo JSON de credenciales descargado
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
# ID de tu proyecto de Google Cloud
GOOGLE_CLOUD_PROJECT=tu-project-id-aqui
# Región de Vertex AI
VERTEX_AI_LOCATION=us-central1

# Django Configuration
# Genera una clave secreta segura
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=True
```

#### 5.3 Generar SECRET_KEY
```bash
# Opción 1: Usar Django
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())

# Opción 2: Usar Python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Paso 6: Configurar Django

#### 6.1 Ejecutar migraciones
```bash
python manage.py migrate
```

#### 6.2 Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

#### 6.3 Verificar configuración
```bash
# Verificar que no hay errores
python manage.py check
```

### Paso 7: Probar la Configuración

#### 7.1 Iniciar servidor de desarrollo
```bash
python manage.py runserver
```

#### 7.2 Verificar funcionamiento
1. Abre tu navegador en `http://localhost:8000`
2. Deberías ver la interfaz del chatbot
3. Prueba enviar un mensaje

### Paso 8: Configuración Adicional (Opcional)

#### 8.1 Configurar logging
El proyecto incluye configuración de logging en `chatbot_project/logging_config.py`. Los logs se guardan en `logs/chatbot.log`.

#### 8.2 Configurar CORS (si usas frontend separado)
En `chatbot_project/settings.py`, agrega tu dominio:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://127.0.0.1:3000",
]
```

## 🚨 Solución de Problemas Comunes

### Error: "No module named 'google.cloud'"
```bash
pip install --upgrade google-cloud-aiplatform
```

### Error: "MongoDB connection failed"
- Verifica que MongoDB esté ejecutándose
- Revisa la URL de conexión en `.env`
- Para Atlas, verifica que tu IP esté en la lista blanca

### Error: "Vertex AI not enabled"
- Verifica que la API esté habilitada en Google Cloud Console
- Confirma que las credenciales sean correctas
- Revisa que el proyecto ID sea correcto

### Error: "Permission denied"
- Verifica que la cuenta de servicio tenga los permisos correctos
- Asegúrate de que el archivo de credenciales sea accesible

### Error: "Invalid SECRET_KEY"
- Genera una nueva clave secreta usando el método del Paso 5.3
- Asegúrate de que no tenga espacios ni caracteres especiales problemáticos

## 🌐 Uso

1. Abre tu navegador y ve a `http://localhost:8000`
2. Comienza a chatear con el bot
3. Todas las conversaciones se guardan automáticamente en MongoDB
4. El historial se recupera cuando regresas a la página

## 📁 Estructura del Proyecto

```
chatbot_project/
├── chatbot_project/          # Configuración principal de Django
│   ├── settings.py          # Configuraciones del proyecto
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── chat/                    # App principal del chat
│   ├── models.py            # Modelos (no se usan, se usa MongoDB)
│   ├── views.py             # Vistas del chat
│   ├── urls.py              # URLs del chat
│   ├── mongodb.py           # Conexión a MongoDB
│   └── langgraph_service.py # Servicio de LangGraph + Vertex AI
├── templates/               # Templates HTML
│   ├── base.html           # Template base
│   └── chat/
│       └── chat.html       # Template principal del chat
├── requirements.txt         # Dependencias de Python
├── env_example.txt         # Ejemplo de variables de entorno
└── README.md               # Este archivo
```

## 🔧 Configuración Avanzada

### Personalizar el Modelo de IA

Puedes modificar el modelo en `chat/langgraph_service.py`:

```python
self.llm = ChatVertexAI(
    model_name="gemini-1.5-flash",  # Cambiar modelo aquí
    project=settings.GOOGLE_CLOUD_PROJECT,
    temperature=0.7,                # Ajustar creatividad
    max_output_tokens=1024         # Ajustar longitud de respuesta
)
```

### Personalizar la Interfaz

Los estilos CSS están en `templates/base.html`. Puedes modificar:
- Colores del tema
- Diseño del chat
- Animaciones
- Responsividad

## 🐛 Solución de Problemas

### Error de conexión a MongoDB
- Verifica que MongoDB esté ejecutándose
- Revisa la URL de conexión en `.env`

### Error de Google Cloud
- Verifica que las credenciales sean correctas
- Asegúrate de que la API de Vertex AI esté habilitada
- Revisa que el proyecto de Google Cloud sea correcto

### Error de CORS
- Si usas un frontend separado, configura CORS en `settings.py`

## 📝 API Endpoints

- `GET /` - Interfaz principal del chat
- `POST /send-message/` - Enviar mensaje al bot
- `POST /get-history/` - Obtener historial de conversación

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - Framework web
- [LangGraph](https://github.com/langchain-ai/langgraph) - Flujo conversacional
- [Google Vertex AI](https://cloud.google.com/vertex-ai) - Modelo de IA
- [MongoDB](https://www.mongodb.com/) - Base de datos
- [Bootstrap](https://getbootstrap.com/) - Framework CSS

