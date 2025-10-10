import React from 'react'
import { Plus, MessageSquare, Trash2, Menu, X, Database } from 'lucide-react'
import './Sidebar.css'

function Sidebar({ chats, currentChatId, onChatSelect, onNewChat, onDeleteChat, onLoadSample, isOpen, onToggle }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    } else if (diffInHours < 168) { // 7 días
      return date.toLocaleDateString('es-ES', { weekday: 'short' })
    } else {
      return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })
    }
  }

  return (
    <>
      {/* Overlay para móvil */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={onToggle}></div>
      )}
      
      <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="sidebar-title">
            <MessageSquare className="sidebar-icon" />
            <h2>MongoChat</h2>
          </div>
          <button className="toggle-btn" onClick={onToggle}>
            {isOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <div className="sidebar-content">
          <button className="new-chat-btn" onClick={onNewChat}>
            <Plus size={20} />
            <span>Nueva conversación</span>
          </button>

          {chats.length === 0 && (
            <button className="sample-data-btn" onClick={onLoadSample}>
              <Database size={20} />
              <span>Cargar datos de ejemplo</span>
            </button>
          )}

          <div className="chats-list">
            <div className="chats-header">
              <h3>Conversaciones</h3>
              {chats.length > 0 && (
                <span className="chats-count">{chats.length}</span>
              )}
            </div>
            {chats.length === 0 ? (
              <div className="empty-state">
                <MessageSquare size={48} />
                <p>No hay conversaciones</p>
                <small>Crea una nueva conversación para comenzar</small>
              </div>
            ) : (
              <div className="chats">
                {chats.map(chat => (
                  <div
                    key={chat.id}
                    className={`chat-item ${currentChatId === chat.id ? 'active' : ''}`}
                    onClick={() => onChatSelect(chat.id)}
                  >
                    <div className="chat-info">
                      <h4>{chat.title}</h4>
                      <div className="chat-meta">
                        <span className="chat-time">{formatDate(chat.createdAt)}</span>
                        {chat.messages && chat.messages.length > 0 && (
                          <span className="message-count">{chat.messages.length} mensajes</span>
                        )}
                      </div>
                    </div>
                    <button
                      className="delete-btn"
                      onClick={(e) => {
                        e.stopPropagation()
                        onDeleteChat(chat.id)
                      }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              <MessageSquare size={20} />
            </div>
            <div className="user-details">
              <span className="user-name">Usuario</span>
              <span className="user-status">En línea</span>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar
