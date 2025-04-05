import {
  AutoFixHigh as AutoFixHighIcon,
  Psychology as PsychologyIcon,
  Layers as LayersIcon,
  BubbleChart as BubbleChartIcon,
  Visibility as VisibilityIcon,
  AutoAwesome as AutoAwesomeIcon,
  QuestionAnswer as QuestionAnswerIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material';
import { FractalFramework, InterventionTypeConfig } from '../types';

export const FRACTAL_FRAMEWORK: FractalFramework = {
  recursiveElaboration: {
    color: '#4CAF50',
    label: 'Recursive Elaboration',
    description: 'Iterative deepening of understanding through self-reflection',
    icon: AutoFixHighIcon,
  },
  transformativeInput: {
    color: '#2196F3',
    label: 'Transformative Input',
    description: 'Novel perspectives or information that catalyze change',
    icon: PsychologyIcon,
  },
  emergentPattern: {
    color: '#FF9800',
    label: 'Emergent Pattern',
    description: 'New insights or understanding that emerge from the process',
    icon: BubbleChartIcon,
  },
  microLevel: {
    color: '#9C27B0',
    label: 'Micro Level',
    description: 'Individual thoughts and immediate reactions',
    icon: LayersIcon,
  },
  mesoLevel: {
    color: '#3F51B5',
    label: 'Meso Level',
    description: 'Patterns across multiple thoughts and interactions',
    icon: BubbleChartIcon,
  },
  macroLevel: {
    color: '#009688',
    label: 'Macro Level',
    description: 'System-level insights and transformations',
    icon: AutoAwesomeIcon,
  },
};

export const interventionTypes: Record<string, InterventionTypeConfig> = {
  awareness: {
    color: '#4CAF50',
    label: 'Awareness Intervention',
    description: 'Drawing attention to patterns or processes',
    icon: VisibilityIcon,
  },
  inquiry: {
    color: '#2196F3',
    label: 'Inquiry Intervention',
    description: 'Questions that promote deeper exploration',
    icon: QuestionAnswerIcon,
  },
  insight: {
    color: '#FF9800',
    label: 'Insight Intervention',
    description: 'Sharing observations that may catalyze new understanding',
    icon: LightbulbIcon,
  },
}; 