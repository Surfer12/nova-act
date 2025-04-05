import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  IconButton,
  Chip,
} from '@mui/material';
import {
  NavigateBefore as NavigateBeforeIcon,
  NavigateNext as NavigateNextIcon,
} from '@mui/icons-material';
import { FRACTAL_FRAMEWORK } from '../utils/framework';
import { Thought, ProcessingLevel } from '../types';

interface FractalThoughtProcessProps {
  onSave: (thought: Thought) => void;
}

const initialThought: Omit<Thought, 'timestamp'> = {
  initialState: '',
  recursiveElaboration: '',
  transformativeInput: '',
  emergentPattern: '',
  processingLevel: 'mesoLevel',
  iterationCount: 1,
};

export const FractalThoughtProcess: React.FC<FractalThoughtProcessProps> = ({ onSave }) => {
  const [step, setStep] = useState(1);
  const [thought, setThought] = useState<Omit<Thought, 'timestamp'>>(initialThought);

  const handleNext = () => {
    if (step < 4) {
      setStep(step + 1);
    } else {
      handleSave();
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSave = () => {
    onSave({
      ...thought,
      timestamp: new Date().toISOString(),
    });
    setThought(initialThought);
    setStep(1);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 2 }}>
              Initial State (z₀)
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
              The starting point of exploration
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              placeholder="Record your initial thought or observation..."
              value={thought.initialState}
              onChange={(e) => setThought({ ...thought, initialState: e.target.value })}
            />
          </Box>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 2, color: FRACTAL_FRAMEWORK.recursiveElaboration.color }}>
              Recursive Elaboration (z²)
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
              Deepen your understanding through self-reflection
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              placeholder="How does this thought connect to or build upon itself?"
              value={thought.recursiveElaboration}
              onChange={(e) => setThought({ ...thought, recursiveElaboration: e.target.value })}
            />
          </Box>
        );
      case 3:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 2, color: FRACTAL_FRAMEWORK.transformativeInput.color }}>
              Transformative Input (c)
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
              Add new perspectives or information
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              placeholder="What new information or perspective shifts your thinking?"
              value={thought.transformativeInput}
              onChange={(e) => setThought({ ...thought, transformativeInput: e.target.value })}
            />
          </Box>
        );
      case 4:
        return (
          <Box>
            <Typography variant="h6" sx={{ mb: 2, color: FRACTAL_FRAMEWORK.emergentPattern.color }}>
              Emergent Pattern (new z)
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
              Synthesize the new understanding that emerges
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              placeholder="What new insight or understanding emerges?"
              value={thought.emergentPattern}
              onChange={(e) => setThought({ ...thought, emergentPattern: e.target.value })}
            />
          </Box>
        );
      default:
        return null;
    }
  };

  const stepFields: (keyof Omit<Thought, 'timestamp' | 'processingLevel' | 'iterationCount'>)[] = [
    'initialState',
    'recursiveElaboration',
    'transformativeInput',
    'emergentPattern'
  ];

  return (
    <Card>
      <CardContent>
        {renderStep()}
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3, alignItems: 'center' }}>
          <IconButton onClick={handleBack} disabled={step === 1}>
            <NavigateBeforeIcon />
          </IconButton>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip
              size="small"
              icon={React.createElement(FRACTAL_FRAMEWORK[thought.processingLevel].icon)}
              label={FRACTAL_FRAMEWORK[thought.processingLevel].label}
              sx={{ bgcolor: `${FRACTAL_FRAMEWORK[thought.processingLevel].color}30` }}
            />
            <Chip
              size="small"
              label={`Iteration ${thought.iterationCount}`}
              sx={{ bgcolor: 'rgba(0,0,0,0.1)' }}
            />
          </Box>

          {step < 4 ? (
            <Button
              variant="contained"
              endIcon={<NavigateNextIcon />}
              onClick={handleNext}
              disabled={!thought[stepFields[step - 1]]}
            >
              Next Step
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              onClick={handleSave}
              disabled={!thought.emergentPattern}
            >
              Complete
            </Button>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}; 