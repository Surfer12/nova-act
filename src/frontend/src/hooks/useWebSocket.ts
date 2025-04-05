import { useEffect, useRef, useState, useCallback } from 'react';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

export const useWebSocket = ({
  url,
  onMessage,
  onOpen,
  onClose,
  onError,
}: UseWebSocketOptions) => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Event | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
      onOpen?.();
    };

    ws.onclose = () => {
      setIsConnected(false);
      onClose?.();
    };

    ws.onerror = (err) => {
      setError(err);
      onError?.(err);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch (err) {
        onMessage?.(event.data);
      }
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [url, onMessage, onOpen, onClose, onError]);

  const sendMessage = useCallback((message: string | object) => {
    if (!wsRef.current || !isConnected) return;
    
    const data = typeof message === 'string' ? message : JSON.stringify(message);
    wsRef.current.send(data);
  }, [isConnected]);

  return {
    isConnected,
    error,
    sendMessage,
  };
}; 