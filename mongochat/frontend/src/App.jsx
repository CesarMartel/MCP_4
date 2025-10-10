import React, { useState, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import { loadSampleData } from './utils/sampleData'
import './App.css'

function App() {
  const [chats, setChats] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth > 768)

  // Cargar chats del localStorage al inicializar
  useEffect(() => {
    const savedChats = localStorage.getItem('mongochat-chats')
    if (savedChats) {
      const parsedChats = JSON.parse(savedChats)
      setChats(parsedChats)
      if (parsedChats.length > 0 && !currentChatId) {
        setCurrentChatId(parsedChats[0].id)
      }
    }
  }, [])

  // Guardar chats en localStorage cuando cambien
  useEffect(() => {
    if (chats.length > 0) {
      localStorage.setItem('mongochat-chats', JSON.stringify(chats))
    }
  }, [chats])

  // Manejar redimensionamiento de ventana
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setIsSidebarOpen(false)
      } else {
        setIsSidebarOpen(true)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const createNewChat = () => {
    const newChat = {
      id: Date.now().toString(),
      title: 'Nueva conversación',
      messages: [],
      createdAt: new Date().toISOString()
    }
    setChats(prev => [newChat, ...prev])
    setCurrentChatId(newChat.id)
  }

  const updateChat = (chatId, messages) => {
    setChats(prev => prev.map(chat => 
      chat.id === chatId 
        ? { ...chat, messages, title: messages.length > 0 ? messages[0].text.substring(0, 30) + '...' : 'Nueva conversación' }
        : chat
    ))
  }

  const deleteChat = (chatId) => {
    setChats(prev => prev.filter(chat => chat.id !== chatId))
    if (currentChatId === chatId) {
      const remainingChats = chats.filter(chat => chat.id !== chatId)
      setCurrentChatId(remainingChats.length > 0 ? remainingChats[0].id : null)
    }
  }

  const loadSampleChats = () => {
    const sampleChats = loadSampleData()
    setChats(sampleChats)
    setCurrentChatId(sampleChats[0].id)
  }

  const handleChatSelect = (chatId) => {
    setCurrentChatId(chatId)
    // Cerrar sidebar en móviles después de seleccionar un chat
    if (window.innerWidth <= 768) {
      setIsSidebarOpen(false)
    }
  }

  const currentChat = chats.find(chat => chat.id === currentChatId)

  return (
    <div className="app">
      <Sidebar 
        chats={chats}
        currentChatId={currentChatId}
        onChatSelect={handleChatSelect}
        onNewChat={createNewChat}
        onDeleteChat={deleteChat}
        onLoadSample={loadSampleChats}
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
      />
      <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
        <ChatInterface 
          chat={currentChat}
          onUpdateChat={updateChat}
          onNewChat={createNewChat}
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          isSidebarOpen={isSidebarOpen}
        />
      </div>
    </div>
  )
}

export default App
