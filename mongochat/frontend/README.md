# MongoChat Frontend

Frontend moderno para el chatbot con MongoDB y Vertex AI.

## Características

- 🎨 **Diseño moderno** con gradientes y animaciones
- 💬 **Interfaz de chat** con mensajes diferenciados (usuario a la derecha, IA a la izquierda)
- 📱 **Responsive** - funciona en móviles y escritorio
- 📚 **Historial de chats** con panel lateral
- 🆕 **Botón de nuevo chat** para iniciar conversaciones
- 🔄 **Tiempo real** - respuestas instantáneas de la IA
- 💾 **Persistencia** - los chats se guardan en localStorage

## Tecnologías

- React 18
- Vite
- Lucide React (iconos)
- CSS moderno con gradientes y animaciones

## Instalación

```bash
npm install
```

## Desarrollo

```bash
npm run dev
```

El frontend se ejecutará en http://localhost:3000

## Producción

```bash
npm run build
```

## Estructura

```
src/
├── components/
│   ├── ChatInterface.jsx    # Interfaz principal del chat
│   ├── ChatInterface.css
│   ├── Message.jsx          # Componente de mensaje individual
│   ├── Message.css
│   ├── Sidebar.jsx          # Panel lateral con historial
│   └── Sidebar.css
├── App.jsx                  # Componente principal
├── App.css
├── main.jsx                 # Punto de entrada
└── index.css                # Estilos globales
```

## Colores

- **Primario**: Gradiente azul-púrpura (#667eea → #764ba2)
- **Fondo**: Gradiente suave
- **Mensajes usuario**: Gradiente primario
- **Mensajes IA**: Blanco con bordes suaves
- **Acentos**: Tonos de gris y azul
