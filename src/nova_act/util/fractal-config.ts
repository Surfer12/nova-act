// src/utils/fractal-config.ts
import yaml from 'js-yaml';

interface FractalConfig {
  transformations: Array<{
    type: string;
    condition: string; // JavaScript condition as string
    transform: string; // JavaScript transform function as string
    params?: Record<string, any>;
  }>;
}

export function loadFractalConfig(yamlContent: string): FractalConfig {
  const config = yaml.load(yamlContent) as FractalConfig;
  
  // Convert string conditions and transforms to functions
  config.transformations = config.transformations.map(transform => ({
    ...transform,
    condition: new Function('thought', `return ${transform.condition}`),
    transform: new Function('thought', `return ${transform.transform}`)
  }));
  
  return config;
}

// Example YAML config:
/*
transformations:
  - type: "recursiveElaboration"
    condition: "thought.processingLevel === 'mesoLevel'"
    transform: "thought.result.split(' ').map(word => ({ word, length: word.length }))"
    params:
      maxDepth: 3
*/