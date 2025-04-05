// src/hooks/useNovaConnection.ts
import { useState, useEffect, useCallback } from 'react';
import { processThoughtForDisplay } from '../utils/fractal-processors';

interface NovaConnectionConfig {
  host?: string;
  port?: number;
  fractalConfig?: FractalConfig;
}

interface FractalConfig {
  transformations: Array<{
    type: string;
    condition: (thought: any) => boolean;
    transform: (thought: any) => any;
    params?: Record<string, any>;
  }>;
}

export function useNovaConnection(config: NovaConnectionConfig = {}) {
  const [thoughts, setThoughts] = useState<any[]>([]);
  const [interventions, setInterventions] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  
  const handleMessage = useCallback((message: any) => {
    try {
      const { type, data } = message;
      
      switch (type) {
        case 'thoughtUpdate':
          setThoughts(prev => [...prev, processThoughtForDisplay(data)]);
          break;
        case 'metaIntervention':
          setInterventions(prev => [...prev, data]);
          break;
        case 'fractalConfigAck':
          console.log('Fractal config received by Nova Act');
          break;
        default:
          console.log('Unknown message type:', type);
      }
    } catch (err) {
      console.error('Error processing message:', err);
    }
  }, []);

  useEffect(() => {
    const ws = new WebSocket(`ws://${config.host || 'localhost'}:${config.port || 8081}`);
    
    ws.onopen = () => {
      setIsConnected(true);
      // Send fractal config if provided
      if (config.fractalConfig) {
        ws.send(JSON.stringify({
          type: 'FRACTAL_CONFIG',
          config: config.fractalConfig
        }));
      }
    };
    
    ws.onclose = () => setIsConnected(false);
    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        handleMessage(message);
      } catch (err) {
        console.error('Error parsing message:', err);
      }
    };
    
    setWs(ws);
    
    return () => {
      ws.close();
    };
  }, [config.host, config.port, config.fractalConfig, handleMessage]);
  
  const sendMetaIntervention = useCallback((intervention: any) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'META_INTERVENTION',
        intervention
      }));
    }
  }, [ws]);
  
  return { 
    thoughts, 
    interventions, 
    isConnected,
    sendMetaIntervention
  };
}