import React from 'react';
import { FractalThoughtProcess } from './components/FractalThoughtProcess';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Fractal Communication Explorer</h1>
        <p>Real-time visualization of Nova Act thought processes and interventions</p>
      </header>
      <main>
        <FractalThoughtProcess />
      </main>
    </div>
  );
}

export default App; 