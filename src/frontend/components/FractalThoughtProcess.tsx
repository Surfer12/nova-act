import React from 'react';
import { useNovaBridge } from '../hooks/useNovaBridge';

export function FractalThoughtProcess() {
  const { thoughts, interventions, isConnected, error, publishIntervention } = useNovaBridge();

  const handleIntervention = async (thoughtId: string) => {
    try {
      await publishIntervention(
        'current-session',
        'patternRecognition',
        'I notice an interesting pattern in this thought process...',
        thoughtId
      );
    } catch (error) {
      console.error('Failed to publish intervention:', error);
    }
  };

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!isConnected) {
    return <div className="loading">Connecting to Nova Bridge...</div>;
  }

  return (
    <div className="fractal-thought-process">
      <h2>Thought Processes</h2>
      <div className="thoughts-list">
        {thoughts.map((thought) => (
          <div key={thought.id} className="thought-card">
            <div className="thought-header">
              <span className="processing-level">{thought.processingLevel}</span>
              <span className="iteration">Iteration {thought.iterationCount}</span>
            </div>
            <div className="thought-content">
              <h3>Initial State</h3>
              <p>{thought.initialState}</p>
              
              <h3>Recursive Elaboration</h3>
              <p>{thought.recursiveElaboration}</p>
              
              <h3>Transformative Input</h3>
              <p>{thought.transformativeInput}</p>
              
              <h3>Emergent Pattern</h3>
              <p>{thought.emergentPattern}</p>
            </div>
            <button
              onClick={() => handleIntervention(thought.id)}
              className="intervention-button"
            >
              Add Intervention
            </button>
          </div>
        ))}
      </div>

      <h2>Interventions</h2>
      <div className="interventions-list">
        {interventions.map((intervention) => (
          <div key={intervention.id} className="intervention-card">
            <div className="intervention-header">
              <span className="type">{intervention.type}</span>
              <span className="processing-level">{intervention.processingLevel}</span>
            </div>
            <p>{intervention.content}</p>
            {intervention.targetThought && (
              <div className="target-thought">
                Target Thought: {intervention.targetThought}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 