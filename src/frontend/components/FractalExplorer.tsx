import React from 'react';
import { useNovaConnection } from '../hooks/useNovaConnection';
import { loadFractalConfig } from '../utils/fractal-config';
import FractalVisualization from './FractalVisualization';

const fractalYaml = `
transformations:
  - type: "recursiveElaboration"
    condition: "thought.processingLevel === 'mesoLevel'"
    transform: "thought.result.split(' ').map(word => ({ word, length: word.length }))"
    params:
      maxDepth: 3
`;

export function FractalExplorer() {
  const fractalConfig = loadFractalConfig(fractalYaml);
  
  const { 
    thoughts, 
    interventions, 
    isConnected,
    sendMetaIntervention 
  } = useNovaConnection({
    host: 'localhost',
    port: 8081,
    fractalConfig
  });
  
  return (
    <div>
      <div>Connection Status: {isConnected ? 'Connected' : 'Disconnected'}</div>
      <FractalVisualization 
        thoughts={thoughts}
        interventions={interventions}
        onIntervention={sendMetaIntervention}
      />
    </div>
  );
}
