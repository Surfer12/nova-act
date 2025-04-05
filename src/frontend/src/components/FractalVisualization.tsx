import React from 'react';
import { Box, Card, CardContent, Typography, Chip } from '@mui/material';
import * as d3 from 'd3';
import { FRACTAL_FRAMEWORK } from '../utils/framework';
import { Thought, ProcessingLevel } from '../types';

interface Point {
  x: number;
  y: number;
  iterations: number;
}

interface ThoughtNode extends Thought {
  x: number;
  y: number;
  color: string;
}

interface FractalVisualizationProps {
  thoughts: Thought[];
}

export function FractalVisualization({ thoughts }: FractalVisualizationProps) {
  const svgRef = React.useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = React.useState<ThoughtNode | null>(null);
  
  React.useEffect(() => {
    if (!thoughts.length || !svgRef.current) return;
    
    // Clear previous visualization
    d3.select(svgRef.current).selectAll("*").remove();
    
    // Setup visualization dimensions
    const width = svgRef.current.clientWidth;
    const height = 600;
    const margin = { top: 10, right: 10, bottom: 10, left: 10 };
    
    // Mandelbrot set parameters
    const MAX_ITERS = 200;
    const min_x = -2.0;
    const max_x = 0.6;
    const min_y = -1.5;
    const max_y = 1.5;
    
    // Create SVG
    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;");
    
    // Create container for the visualization
    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Scale functions for mapping coordinates
    const xScale = d3.scaleLinear()
      .domain([min_x, max_x])
      .range([0, width - margin.left - margin.right]);
    
    const yScale = d3.scaleLinear()
      .domain([min_y, max_y])
      .range([height - margin.top - margin.bottom, 0]);

    // Create a canvas element for better performance with the Mandelbrot set
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d')!;
    const imageData = ctx.createImageData(width, height);
    
    // Higher resolution for Mandelbrot set
    const resolution = 1; // 1 pixel per point for maximum detail
    const cols = Math.floor(width / resolution);
    const rows = Math.floor(height / resolution);
    
    // Function to compute Mandelbrot set iterations
    function mandelbrotIterations(cx: number, cy: number): number {
      let x = 0;
      let y = 0;
      let iteration = 0;
      
      while (x * x + y * y <= 4 && iteration < MAX_ITERS) {
        const xtemp = x * x - y * y + cx;
        y = 2 * x * y + cy;
        x = xtemp;
        iteration++;
      }
      
      return iteration;
    }
    
    // Compute and render Mandelbrot set
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const x = min_x + (j / cols) * (max_x - min_x);
        const y = min_y + (i / rows) * (max_y - min_y);
        const iterations = mandelbrotIterations(x, y);
        
        // Convert iterations to color using a custom color scheme
        let color;
        if (iterations === MAX_ITERS) {
          color = [0, 0, 0, 255]; // Black for the Mandelbrot set
        } else {
          // Smooth coloring algorithm
          const t = iterations / MAX_ITERS;
          const r = Math.floor(9 * (1 - t) * t * t * t * 255);
          const g = Math.floor(15 * (1 - t) * (1 - t) * t * t * 255);
          const b = Math.floor(8.5 * (1 - t) * (1 - t) * (1 - t) * t * 255);
          color = [r, g, b, 255];
        }
        
        // Set pixel in ImageData
        const pixelIndex = (i * width + j) * 4;
        imageData.data[pixelIndex] = color[0];     // R
        imageData.data[pixelIndex + 1] = color[1]; // G
        imageData.data[pixelIndex + 2] = color[2]; // B
        imageData.data[pixelIndex + 3] = color[3]; // A
      }
    }
    
    // Put the ImageData on the canvas
    ctx.putImageData(imageData, 0, 0);
    
    // Convert canvas to image and add to SVG
    const image = new Image();
    image.src = canvas.toDataURL();
    
    // Add the Mandelbrot set as a background image
    svg.append("image")
      .attr("width", width)
      .attr("height", height)
      .attr("preserveAspectRatio", "none")
      .attr("xlink:href", image.src)
      .style("opacity", 0.5); // Adjust opacity to make it more visible but not overwhelming

    // Map thoughts to complex plane
    const thoughtNodes: ThoughtNode[] = thoughts.map((thought: Thought, i: number) => {
      // Map thought properties to Mandelbrot set coordinates
      const iterationFactor = thought.iterationCount / Math.max(...thoughts.map((t: Thought) => t.iterationCount));
      
      // Calculate position based on the Mandelbrot set formula z = z² + c
      // Use thought properties to determine position in the interesting regions of the set
      let x, y;
      
      if (thought.processingLevel === 'microLevel') {
        // Position in the main cardioid
        const t = (2 * Math.PI * i) / thoughts.length;
        const r = 0.25 * (1 - Math.cos(t));
        x = 0.25 * Math.cos(t) * r + iterationFactor * 0.1;
        y = 0.25 * Math.sin(t) * r;
      } else if (thought.processingLevel === 'mesoLevel') {
        // Position in the period-2 bulb
        const t = (2 * Math.PI * i) / thoughts.length;
        x = -1 + 0.25 * Math.cos(t) * iterationFactor;
        y = 0.25 * Math.sin(t) * iterationFactor;
      } else {
        // Position in other interesting regions
        const t = (2 * Math.PI * i) / thoughts.length;
        const bulbIndex = i % 3;
        const bulbOffset = [-0.5, -1.25, -1.75][bulbIndex];
        x = bulbOffset + 0.15 * Math.cos(t) * iterationFactor;
        y = 0.15 * Math.sin(t) * iterationFactor;
      }
      
      return {
        ...thought,
        x: xScale(x),
        y: yScale(y),
        color: FRACTAL_FRAMEWORK[thought.processingLevel as ProcessingLevel].color
      };
    });
    
    // Draw connecting lines between sequential thoughts with curves
    g.selectAll(".thought-connection")
      .data(thoughtNodes.slice(1))
      .join("path")
      .attr("class", "thought-connection")
      .attr("d", (d: ThoughtNode, i: number) => {
        const source = thoughtNodes[i];
        const target = d;
        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;
        // Create a curved path between points
        return `M ${source.x} ${source.y} 
                Q ${midX} ${midY} ${target.x} ${target.y}`;
      })
      .attr("stroke", (d: ThoughtNode) => d.color)
      .attr("stroke-width", 1)
      .attr("fill", "none")
      .attr("opacity", 0.5);

    // Draw thought nodes with labels
    const nodes = g.selectAll(".thought-node")
      .data(thoughtNodes)
      .join("g")
      .attr("class", "thought-node")
      .attr("transform", (d: ThoughtNode) => `translate(${d.x},${d.y})`)
      .on("click", (event: MouseEvent, d: ThoughtNode) => {
        setSelectedNode(d);
        event.stopPropagation();
      });
    
    // Add circles for thoughts with glowing effect
    nodes.append("circle")
      .attr("r", 12)
      .attr("class", "glow")
      .attr("fill", "none")
      .attr("stroke", (d: ThoughtNode) => d.color)
      .attr("stroke-width", 2)
      .attr("filter", "url(#glow)");
      
    nodes.append("circle")
      .attr("r", 8)
      .attr("fill", (d: ThoughtNode) => d.color)
      .attr("stroke", "#fff")
      .attr("stroke-width", 2);

    // Add glow filter
    const defs = svg.append("defs");
    const filter = defs.append("filter")
      .attr("id", "glow")
      .attr("x", "-50%")
      .attr("y", "-50%")
      .attr("width", "200%")
      .attr("height", "200%");
    
    filter.append("feGaussianBlur")
      .attr("stdDeviation", "3")
      .attr("result", "coloredBlur");
    
    const feMerge = filter.append("feMerge");
    feMerge.append("feMergeNode")
      .attr("in", "coloredBlur");
    feMerge.append("feMergeNode")
      .attr("in", "SourceGraphic");
  }, [thoughts]);
  
  return (
    <Box sx={{ position: "relative", width: "100%", height: "600px", mt: 4 }}>
      <svg
        ref={svgRef}
        style={{ width: "100%", height: "100%", backgroundColor: "#000" }}
        onClick={() => setSelectedNode(null)}
      />
      
      {selectedNode && (
        <Card sx={{ 
          position: "absolute", 
          top: 20, 
          right: 20, 
          maxWidth: 350, 
          backgroundColor: "rgba(0,0,0,0.8)",
          color: "#fff",
          border: `1px solid ${selectedNode.color || "#fff"}`
        }}>
          <CardContent>
            <Typography variant="h6" sx={{ color: selectedNode.color || "#fff" }}>
              {selectedNode.initialState?.substring(0, 50)}
            </Typography>
            
            {selectedNode.recursiveElaboration && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" sx={{ color: FRACTAL_FRAMEWORK.recursiveElaboration.color }}>
                  Recursive Elaboration (z²):
                </Typography>
                <Typography variant="body2" sx={{ mt: 0.5, color: "#fff" }}>
                  {selectedNode.recursiveElaboration}
                </Typography>
              </Box>
            )}
            
            {selectedNode.transformativeInput && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" sx={{ color: FRACTAL_FRAMEWORK.transformativeInput.color }}>
                  Transformative Input (c):
                </Typography>
                <Typography variant="body2" sx={{ mt: 0.5, color: "#fff" }}>
                  {selectedNode.transformativeInput}
                </Typography>
              </Box>
            )}
            
            {selectedNode.emergentPattern && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" sx={{ color: FRACTAL_FRAMEWORK.emergentPattern.color }}>
                  Emergent Pattern (new z):
                </Typography>
                <Typography variant="body2" sx={{ mt: 0.5, color: "#fff" }}>
                  {selectedNode.emergentPattern}
                </Typography>
              </Box>
            )}
            
            <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
              <Chip 
                size="small"
                label={`Iteration ${selectedNode.iterationCount || 1}`}
                sx={{ 
                  bgcolor: 'rgba(255,255,255,0.1)',
                  color: '#fff',
                  border: '1px solid rgba(255,255,255,0.3)'
                }}
              />
              <Chip 
                size="small"
                label={FRACTAL_FRAMEWORK[selectedNode.processingLevel as ProcessingLevel].label}
                sx={{ 
                  bgcolor: `${selectedNode.color}30`,
                  color: selectedNode.color,
                  border: `1px solid ${selectedNode.color}`
                }}
              />
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
} 