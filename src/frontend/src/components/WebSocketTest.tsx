import React, { useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export const WebSocketTest: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [inputMessage, setInputMessage] = useState('');

  const { isConnected, error, sendMessage } = useWebSocket({
    url: 'ws://localhost:8081',
    onMessage: (data) => {
      setMessages(prev => [...prev, typeof data === 'string' ? data : JSON.stringify(data)]);
    },
    onOpen: () => {
      setMessages(prev => [...prev, 'Connected to WebSocket server']);
    },
    onClose: () => {
      setMessages(prev => [...prev, 'Disconnected from WebSocket server']);
    },
    onError: (err) => {
      setMessages(prev => [...prev, `Error: ${err.type}`]);
    },
  });

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      sendMessage(inputMessage);
      setInputMessage('');
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <div className="text-sm font-semibold mb-2">
          Status: {isConnected ? 
            <span className="text-green-600">Connected</span> : 
            <span className="text-red-600">Disconnected</span>
          }
        </div>
        {error && (
          <div className="text-red-600 text-sm">
            Error: {error.type}
          </div>
        )}
      </div>

      <form onSubmit={handleSend} className="mb-4 flex gap-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type a message..."
          className="flex-1 px-3 py-2 border rounded"
        />
        <button
          type="submit"
          disabled={!isConnected}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Send
        </button>
      </form>

      <div className="border rounded p-4 h-64 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className="mb-2">
            {msg}
          </div>
        ))}
      </div>
    </div>
  );
}; 