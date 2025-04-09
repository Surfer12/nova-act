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
  processingLevel: ProcessingLevel;
  iterationCount: number;
}

interface Intervention {
  id: string;
  sessionId: string;
  timestamp: string;
  type: InterventionType;
  content: string;
  targetThought?: string;
  processingLevel: ProcessingLevel;
}

type ProcessingLevel = 'microLevel' | 'mesoLevel' | 'macroLevel';
type InterventionType = 'thoughtUpdate' | 'interventionUpdate';

interface BridgeState {
  thoughts: Thought[];
  interventions: Intervention[];
  isConnected: boolean;
  error: string | null;
}

interface BridgeMessage {
  eventType: InterventionType;
  data: Thought | Intervention;
}

interface PublishInterventionParams {
  sessionId: string;
  type: string;
  content: string;
  targetThought?: string;
  processingLevel?: ProcessingLevel;
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
        return;
      }

      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        updateState(draft => {
          draft.isConnected = true;
          draft.error = null;
        });
      };

      ws.onclose = (event: CloseEvent) => {
        updateState(draft => {
          draft.isConnected = false;
          draft.error = `Connection closed${event.wasClean ? ' cleanly' : ''}. Code: ${event.code}`;
        });
        reconnectTimeout = setTimeout(connect, 5000);
      };

      ws.onerror = (error: Event) => {
        updateState(draft => {
          draft.error = `WebSocket error: ${error instanceof ErrorEvent ? error.message : 'Unknown error'}`;
        });
      };

      ws.onmessage = (event: MessageEvent) => {
        try {
          const message = JSON.parse(event.data) as BridgeMessage;
          handleMessage(message);
        } catch (error) {
          updateState(draft => {
            draft.error = `Error parsing message: ${error instanceof Error ? error.message : 'Unknown error'}`;
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
  }, [wsUrl, handleMessage, updateState]);

  const publishIntervention = useCallback(async ({
    sessionId,
    type,
    content,
    targetThought,
    processingLevel = 'mesoLevel'
  }: PublishInterventionParams): Promise<Response> => {
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

      return response;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to publish intervention';
      updateState(draft => {
        draft.error = errorMessage;
      });
      throw error;
    }
  }, [updateState]);

  return {
    ...state,
    publishIntervention
  };
} 