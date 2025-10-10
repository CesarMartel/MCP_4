import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Plus, Menu } from 'lucide-react'
import Message from './Message'
import './ChatInterface.css'

function ChatInterface({ chat, onUpdateChat, onNewChat, onToggleSidebar, isSidebarOpen }) {
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chat?.messages])

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [chat])

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      text: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date().toISOString()
    }

    const updatedMessages = [...(chat?.messages || []), userMessage]
    onUpdateChat(chat.id, updatedMessages)
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${encodeURIComponent(inputMessage.trim())}`
      })

      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor')
      }

      const data = await response.json()
      
      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: data.reply,
        sender: 'bot',
        timestamp: new Date().toISOString()
      }

      const finalMessages = [...updatedMessages, botMessage]
      onUpdateChat(chat.id, finalMessages)
    } catch (error) {
      console.error('Error al enviar mensaje:', error)
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, inténtalo de nuevo.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true
      }
      const finalMessages = [...updatedMessages, errorMessage]
      onUpdateChat(chat.id, finalMessages)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!chat) {
    return (
      <div className="chat-interface no-chat">
        <div className="welcome-screen">
          <div className="welcome-content">
            <Bot size={64} className="welcome-icon" />
            <h1>¡Bienvenido a MongoChat!</h1>
            <p>Tu asistente de IA personalizado con Vertex AI</p>
            <button className="start-chat-btn" onClick={onNewChat}>
              <Plus size={20} />
              <span>Comenzar nueva conversación</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-header-left">
          <button 
            className={`menu-toggle-btn ${isSidebarOpen ? 'active' : ''}`} 
            onClick={onToggleSidebar}
            title={isSidebarOpen ? 'Cerrar historial' : 'Abrir historial'}
          >
            <Menu size={20} />
            {isSidebarOpen && <div className="active-indicator"></div>}
          </button>
          <div className="chat-title">
            <Bot size={24} />
            <h2>{chat.title}</h2>
          </div>
        </div>
        <button className="new-chat-header-btn" onClick={onNewChat}>
          <Plus size={20} />
          <span>Nuevo chat</span>
        </button>
      </div>

      <div className="messages-container">
        {chat.messages.length === 0 ? (
          <div className="empty-chat">
            <Bot size={48} />
            <h3>¡Hola! Soy tu asistente de IA</h3>
            <p>Pregúntame cualquier cosa y te ayudaré con gusto</p>
          </div>
        ) : (
          <div className="messages">
            {chat.messages.map((message) => (
              <Message key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje aquí..."
            className="message-input"
            rows="1"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
