import { useEffect, useRef, useState, useCallback } from 'react';

export interface UseWebSocketOptions<T = unknown> {
  url: string;
  onMessage?: (data: T) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

export interface UseWebSocketResult {
  isConnected: boolean;
  error: Event | null;
  sendMessage: (message: string | object) => void;
}

/**
 * Custom hook for managing WebSocket connections with TypeScript support.
 * @template T - Type of the expected message data
 * @param options - Configuration options for the WebSocket connection
 * @returns WebSocket connection state and control functions
 */
export const useWebSocket = <T = unknown>({
  url,
  onMessage,
  onOpen,
  onClose,
  onError,
}: UseWebSocketOptions<T>): UseWebSocketResult => {
  const [isConnected, setIsConnected] = useState<boolean>(false);
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

    ws.onerror = (err: Event) => {
      setError(err);
      onError?.(err);
    };

    ws.onmessage = (event: MessageEvent) => {
      try {
        const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
        onMessage?.(data as T);
      } catch (err) {
        // If parsing fails, pass the raw data
        onMessage?.(event.data as T);
      }
    };

    wsRef.current = ws;

    // Cleanup function
    return () => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.close();
      }
    };
  }, [url, onMessage, onOpen, onClose, onError]);

  const sendMessage = useCallback((message: string | object): void => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket is not connected. Message not sent:', message);
      return;
    }
    
    try {
      const data = typeof message === 'string' ? message : JSON.stringify(message);
      wsRef.current.send(data);
    } catch (err) {
      console.error('Error sending WebSocket message:', err);
      if (err instanceof Error) {
        setError(new ErrorEvent('error', { error: err, message: err.message }));
      }
    }
  }, []);

  return {
    isConnected,
    error,
    sendMessage,
  };
}; 