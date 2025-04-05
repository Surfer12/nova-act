import { useCallback, useEffect } from 'react';
import { useImmer } from 'use-immer';

interface Thought {
  id: string;
  content: string;
  timestamp: string;
  processingLevel: string;
}

interface Intervention {
  id: string;
  type: string;
  content: string;
  timestamp: string;
  targetThought?: string;
  processingLevel: string;
}

interface BridgeMessage {
  eventType: 'thoughtUpdate' | 'interventionUpdate';
  data: Thought | Intervention;
}

interface BridgeState {
  thoughts: Thought[];
  interventions: Intervention[];
  isConnected: boolean;
  error: string | null;
}

export function useNovaBridge(wsUrl: string = 'ws://localhost:8081') {
  const [state, updateState] = useImmer<BridgeState>({
    thoughts: [],
    interventions: [],
    isConnected: false,
    error: null
  });

  const handleMessage = useCallback((message: BridgeMessage) => {
    updateState(draft => {
      switch (message.eventType) {
        case 'thoughtUpdate':
          draft.thoughts.push(message.data as Thought);
          break;
        case 'interventionUpdate':
          draft.interventions.push(message.data as Intervention);
          break;
      }
    });
  }, [updateState]);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    const connect = () => {
      if (ws?.readyState === WebSocket.CONNECTING) {
        return; // Don't try to connect if already connecting
      }

      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        updateState(draft => {
          draft.isConnected = true;
          draft.error = null;
        });
        console.log('Connected to WebSocket server');
      };

      ws.onclose = (event) => {
        updateState(draft => {
          draft.isConnected = false;
          draft.error = `Connection closed${event.wasClean ? ' cleanly' : ''}. Code: ${event.code}`;
        });
        // Attempt to reconnect after 5 seconds
        reconnectTimeout = setTimeout(connect, 5000);
      };

      ws.onerror = (error) => {
        updateState(draft => {
          draft.error = `WebSocket error: ${error.type}. Please ensure the server is running on port 8081.`;
        });
        console.error('WebSocket error:', error);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as BridgeMessage;
          handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          updateState(draft => {
            draft.error = 'Error parsing message from server';
          });
        }
      };
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [wsUrl, handleMessage]);

  const publishIntervention = useCallback(async (
    sessionId: string,
    type: string,
    content: string,
    targetThought?: string,
    processingLevel: string = 'mesoLevel'
  ) => {
    try {
      const response = await fetch('http://localhost:8081/api/interventions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sessionId,
          type,
          content,
          targetThought,
          processingLevel
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to publish intervention: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error publishing intervention:', error);
      updateState(draft => {
        draft.error = error instanceof Error ? error.message : 'Failed to publish intervention';
      });
      throw error;
    }
  }, [updateState]);

  return {
    ...state,
    publishIntervention
  };
} 