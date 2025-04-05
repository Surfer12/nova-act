import { useEffect, useCallback, useState } from 'react';
import { useImmer } from 'use-immer';

interface Thought {
  id: string;
  sessionId: string;
  timestamp: string;
  initialState: string;
  recursiveElaboration: string;
  transformativeInput: string;
  emergentPattern: string;
  processingLevel: string;
  iterationCount: number;
}

interface Intervention {
  id: string;
  sessionId: string;
  timestamp: string;
  type: string;
  content: string;
  targetThought?: string;
  processingLevel: string;
}

interface BridgeState {
  thoughts: Thought[];
  interventions: Intervention[];
  isConnected: boolean;
  error: string | null;
}

interface BridgeMessage {
  eventType: 'thoughtUpdate' | 'interventionUpdate';
  data: Thought | Intervention;
}

export function useNovaBridge(wsUrl: string = 'ws://localhost:8080/ws') {
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

    const connect = () => {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        updateState(draft => {
          draft.isConnected = true;
          draft.error = null;
        });
      };

      ws.onclose = () => {
        updateState(draft => {
          draft.isConnected = false;
        });
        // Attempt to reconnect after 5 seconds
        setTimeout(connect, 5000);
      };

      ws.onerror = (error) => {
        updateState(draft => {
          draft.error = 'WebSocket connection error';
        });
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as BridgeMessage;
          handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
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
      const response = await fetch('http://localhost:8080/api/interventions', {
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
        throw new Error('Failed to publish intervention');
      }

      return await response.json();
    } catch (error) {
      console.error('Error publishing intervention:', error);
      throw error;
    }
  }, []);

  return {
    ...state,
    publishIntervention
  };
} 