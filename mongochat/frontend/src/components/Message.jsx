import React from 'react'
import { Bot, User } from 'lucide-react'
import './Message.css'

function Message({ message }) {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatText = (text) => {
    // Convertir URLs a enlaces
    const urlRegex = /(https?:\/\/[^\s]+)/g
    const parts = text.split(urlRegex)
    
    return parts.map((part, index) => {
      if (urlRegex.test(part)) {
        return (
          <a 
            key={index} 
            href={part} 
            target="_blank" 
            rel="noopener noreferrer"
            className="message-link"
          >
            {part}
          </a>
        )
      }
      return part
    })
  }

  const isUser = message.sender === 'user'
  const isError = message.isError

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'} ${isError ? 'error-message' : ''}`}>
      <div className="message-avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      <div className="message-content">
        <div className="message-bubble">
          <div className="message-text">
            {formatText(message.text)}
          </div>
          <div className="message-time">
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Message
