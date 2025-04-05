import React from 'react';
import './App.css';
import { useNovaBridge } from '../hooks/useNovaBridge';

function App() {
  const { thoughts, interventions, isConnected, error } = useNovaBridge('ws://localhost:8081');

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold p-4 border-b">NovaAct Fractal Communication Explorer</h1>
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
                Error: {error}
              </div>
            )}
          </div>

          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-semibold mb-2">Thoughts</h2>
              <div className="border rounded p-4 h-48 overflow-y-auto">
                {thoughts.map((thought) => (
                  <div key={thought.id} className="mb-2 p-2 bg-gray-50 rounded">
                    <div className="font-medium">{thought.initialState}</div>
                    <div className="text-sm text-gray-600">{thought.emergentPattern}</div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-lg font-semibold mb-2">Interventions</h2>
              <div className="border rounded p-4 h-48 overflow-y-auto">
                {interventions.map((intervention) => (
                  <div key={intervention.id} className="mb-2 p-2 bg-gray-50 rounded">
                    <div className="font-medium">{intervention.type}</div>
                    <div className="text-sm text-gray-600">{intervention.content}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 