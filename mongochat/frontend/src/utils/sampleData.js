// Datos de ejemplo para demostrar el historial de chats
export const sampleChats = [
  {
    id: '1',
    title: '¿Qué es la inteligencia artificial?',
    messages: [
      {
        id: '1-1',
        text: '¿Qué es la inteligencia artificial?',
        sender: 'user',
        timestamp: new Date(Date.now() - 3600000).toISOString()
      },
      {
        id: '1-2',
        text: 'La inteligencia artificial (IA) es un campo de la informática que se centra en la creación de sistemas informáticos capaces de realizar tareas que normalmente requieren inteligencia humana.',
        sender: 'bot',
        timestamp: new Date(Date.now() - 3590000).toISOString()
      }
    ],
    createdAt: new Date(Date.now() - 3600000).toISOString()
  },
  {
    id: '2',
    title: 'Recetas de cocina',
    messages: [
      {
        id: '2-1',
        text: '¿Cómo hago una pizza casera?',
        sender: 'user',
        timestamp: new Date(Date.now() - 7200000).toISOString()
      },
      {
        id: '2-2',
        text: 'Para hacer una pizza casera necesitas: masa, salsa de tomate, queso mozzarella y tus ingredientes favoritos. Primero prepara la masa, luego añade la salsa y el queso, y finalmente hornea a 200°C por 15-20 minutos.',
        sender: 'bot',
        timestamp: new Date(Date.now() - 7190000).toISOString()
      }
    ],
    createdAt: new Date(Date.now() - 7200000).toISOString()
  },
  {
    id: '3',
    title: 'Programación en Python',
    messages: [
      {
        id: '3-1',
        text: '¿Cómo creo una lista en Python?',
        sender: 'user',
        timestamp: new Date(Date.now() - 86400000).toISOString()
      },
      {
        id: '3-2',
        text: 'En Python puedes crear una lista de varias formas:\n\n1. Lista vacía: `mi_lista = []`\n2. Con elementos: `mi_lista = [1, 2, 3]`\n3. Usando list(): `mi_lista = list()`',
        sender: 'bot',
        timestamp: new Date(Date.now() - 86390000).toISOString()
      }
    ],
    createdAt: new Date(Date.now() - 86400000).toISOString()
  }
]

// Función para cargar datos de ejemplo
export const loadSampleData = () => {
  localStorage.setItem('mongochat-chats', JSON.stringify(sampleChats))
  return sampleChats
}
