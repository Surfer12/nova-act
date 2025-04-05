import { SvgIconComponent } from '@mui/icons-material';

export interface Thought {
  id?: string;
  sessionId?: string;
  timestamp: string;
  initialState: string;
  recursiveElaboration: string;
  transformativeInput: string;
  emergentPattern: string;
  processingLevel: ProcessingLevel;
  iterationCount: number;
}

export type ProcessingLevel = 'microLevel' | 'mesoLevel' | 'macroLevel';

export interface FrameworkElement {
  color: string;
  label: string;
  description: string;
  icon: SvgIconComponent;
}

export interface FractalFramework {
  recursiveElaboration: FrameworkElement;
  transformativeInput: FrameworkElement;
  emergentPattern: FrameworkElement;
  microLevel: FrameworkElement;
  mesoLevel: FrameworkElement;
  macroLevel: FrameworkElement;
}

export interface Intervention {
  id?: string;
  sessionId?: string;
  timestamp: string;
  type: InterventionType;
  content: string;
  targetThought?: string;
  processingLevel: ProcessingLevel;
}

export type InterventionType = 'awareness' | 'inquiry' | 'insight';

export interface InterventionTypeConfig {
  color: string;
  label: string;
  description: string;
  icon: SvgIconComponent;
} 