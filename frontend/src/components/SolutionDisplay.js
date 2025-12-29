import React, { useEffect, useRef, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Divider,
  Alert,
  Chip,
  Card,
  CardContent,
  Button,
  Collapse,
  IconButton,
} from '@mui/material';
import mermaid from 'mermaid';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArchitectureIcon from '@mui/icons-material/Architecture';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ExtensionIcon from '@mui/icons-material/Extension';
import SecurityIcon from '@mui/icons-material/Security';
import BuildIcon from '@mui/icons-material/Build';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import ApiIcon from '@mui/icons-material/Api';
import CodeIcon from '@mui/icons-material/Code';
import NotesIcon from '@mui/icons-material/Notes';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

const SECTIONS = {
  REQUIREMENTS: 'requirements',
  ARCHITECTURE: 'architecture',
  DIAGRAM: 'diagram',
  COMPONENTS: 'components',
  NFR: 'nfr',
  TECH: 'tech',
  COST: 'cost',
  API: 'api',
  IAC: 'iac',
  NOTES: 'notes',
};


const SolutionDisplay = ({ solution }) => {
  const mermaidRef = useRef(null);
  const [showRawDiagram, setShowRawDiagram] = useState(false);
  const [diagramError, setDiagramError] = useState(null);
  const [copySuccess, setCopySuccess] = useState(false);
  const [activeSection, setActiveSection] = useState(SECTIONS.REQUIREMENTS);


  useEffect(() => {
    // Initialize mermaid once
    mermaid.initialize({ 
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#3b82f6',
        primaryTextColor: '#000000',
        primaryBorderColor: '#2563eb',
        lineColor: '#374151',
        secondaryColor: '#8b5cf6',
        secondaryTextColor: '#000000',
        tertiaryColor: '#f3f4f6',
        tertiaryTextColor: '#000000',
        background: '#ffffff',
        mainBkg: '#ffffff',
        textColor: '#000000',
        labelTextColor: '#000000',
        nodeBorder: '#2563eb',
        nodeTextColor: '#000000',
        clusterBkg: '#e0e7ff',
        clusterBorder: '#3b82f6',
        edgeLabelBackground: '#ffffff',
        fontSize: '14px',
        fontFamily: 'Arial, sans-serif',
      },
      securityLevel: 'loose',
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
        nodeSpacing: 50,
        rankSpacing: 50,
      },
    });
  }, []);

  useEffect(() => {
    const renderDiagram = async () => {
      if (solution?.mermaid_diagram && mermaidRef.current) {
        try {
          // Clear previous content and error
          mermaidRef.current.innerHTML = '';
          setDiagramError(null);
          
          // Create a container div with the mermaid class
          const diagramDiv = document.createElement('div');
          diagramDiv.className = 'mermaid';
          diagramDiv.textContent = solution.mermaid_diagram;
          
          // Append to the ref container
          mermaidRef.current.appendChild(diagramDiv);
          
          // Run mermaid to render the diagram
          await mermaid.run({
            nodes: [diagramDiv],
          });
        } catch (error) {
          console.error('Error rendering mermaid diagram:', error);
          setDiagramError(error.message);
          mermaidRef.current.innerHTML = '';
        }
      }
    };

    renderDiagram();
  }, [solution, activeSection]);

  const handleCopyDiagram = () => {
    if (solution?.mermaid_diagram) {
      navigator.clipboard.writeText(solution.mermaid_diagram);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };



  return (
    <Box>
      <Alert 
        icon={<CheckCircleIcon fontSize="inherit" />} 
        severity="success"
        
        sx={{ mb: 3 }}
      >
        Solution Design Successfully Generated
      </Alert>
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {Object.values(SECTIONS).map((section) => (
            <Button
              key={section}
              size="small"
              variant={activeSection === section ? 'contained' : 'outlined'}
              onClick={() => setActiveSection(section)}
            >
              {section.toUpperCase()}
            </Button>
          ))}
        </Box>
      </Paper>

      {/* Normalized Requirements */}
      {
      activeSection === SECTIONS.REQUIREMENTS && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <AccountTreeIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             2️⃣ Normalized Understanding of Requirements
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {JSON.stringify(solution.normalized_requirements, null, 2)}
        </Box>
      </Paper>
      )}

      <Divider sx={{ my: 3 }} />

      {/* Architecture Description */}
      {
        activeSection === SECTIONS.ARCHITECTURE && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ArchitectureIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             3️⃣ Architecture Overview
          </Typography>
        </Box>
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {solution.architecture_description || 'No description provided.'}
        </Typography>
      </Paper>
      )}
      {/* Mermaid Diagram */}
      {
      activeSection === SECTIONS.DIAGRAM && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccountTreeIcon sx={{ mr: 1 }} />
            <Typography variant="h6">
               4️⃣ Architecture Diagram (Visual)
            </Typography>
          </Box>
          {solution.mermaid_diagram && (
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                size="small"
                startIcon={<ContentCopyIcon />}
                onClick={handleCopyDiagram}
                variant="outlined"
              >
                {copySuccess ? 'Copied!' : 'Copy Code'}
              </Button>
              <Button
                size="small"
                endIcon={<ExpandMoreIcon sx={{ transform: showRawDiagram ? 'rotate(180deg)' : 'rotate(0deg)', transition: '0.3s' }} />}
                onClick={() => setShowRawDiagram(!showRawDiagram)}
                variant="outlined"
              >
                {showRawDiagram ? 'Hide' : 'Show'} Raw Code
              </Button>
            </Box>
          )}
        </Box>
        
        {solution.mermaid_diagram ? (
          <>
            {diagramError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Error rendering diagram:</strong>
                </Typography>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', mb: 1 }}>
                  {diagramError}
                </Typography>
                <Typography variant="body2">
                  The diagram code has been sanitized but may still contain syntax errors. 
                  Please check the raw code below or try regenerating the design.
                </Typography>
              </Alert>
            )}
            
            <Collapse in={showRawDiagram}>
              <Box 
                component="pre" 
                sx={{ 
                  backgroundColor: '#1e1e1e', 
                  color: '#d4d4d4',
                  p: 2, 
                  borderRadius: 1,
                  overflow: 'auto',
                  fontSize: '0.875rem',
                  mb: 2,
                  maxHeight: '300px',
                }}
              >
                {solution.mermaid_diagram}
              </Box>
            </Collapse>
            
            <Box 
              ref={mermaidRef}
              sx={{ 
                display: 'flex', 
                justifyContent: 'center',
                p: 2,
                backgroundColor: '#ffffff',
                borderRadius: 1,
                overflow: 'auto',
                minHeight: diagramError ? '100px' : '200px',
                '& svg': {
                  maxWidth: '100%',
                  height: 'auto',
                },
                '& .node text, & .edgeLabel text, & text': {
                  fill: '#000000 !important',
                  fontWeight: '500 !important',
                  fontSize: '14px !important',
                },
                '& .label': {
                  color: '#000000 !important',
                },
              }}
            />
          </>
        ) : (
          <Alert severity="warning">No diagram available</Alert>
        )}
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />

      {/* Components */}
      {activeSection === SECTIONS.COMPONENTS && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ExtensionIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             5️⃣ Key Components and Cloud Services
          </Typography>
        </Box>
        {solution.components?.map((component, index) => (
          <Card key={index} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔹 {component.name} <Chip label={component.type} size="small" sx={{ ml: 1 }} />
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                ☁️ Service: <strong>{component.cloud_service || 'N/A'}</strong>
              </Typography>
              <Typography variant="body2">
                📄 {component.description || 'No description'}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Paper>
      )}

      {/* Non-Functional Requirements */}
      {activeSection === SECTIONS.NFR && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SecurityIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             6️⃣ Non-Functional Requirements
          </Typography>
        </Box>
        {solution.non_functional_considerations?.length > 0 ? (
          <Box component="ul" sx={{ pl: 2 }}>
            {solution.non_functional_considerations.map((item, index) => (
              <Typography component="li" key={index} variant="body1" sx={{ mb: 1 }}>
                ✔️ {item}
              </Typography>
            ))}
          </Box>
        ) : (
          <Typography>No details provided.</Typography>
        )}
      </Paper>
      )}
      {/* Tech Stack */}
      {activeSection === SECTIONS.TECH && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <BuildIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             7️⃣ Proposed Tech Stack
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {solution.tech_stack?.length > 0 ? (
            solution.tech_stack.map((tech, index) => (
              <Chip key={index} label={tech} color="primary" variant="outlined" />
            ))
          ) : (
            <Typography>No tech stack generated.</Typography>
          )}
        </Box>
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />
      
      {/* Cost Estimate */}
      {activeSection === SECTIONS.COST && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <AttachMoneyIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             8️⃣ Estimated Cloud Cost Breakdown
          </Typography>
        </Box>
        <Typography variant="h5" gutterBottom color="primary">
          💵 Total Estimated Monthly Cost: ${solution.cost_estimate?.total_monthly_usd?.toFixed(2) || '0.00'}
        </Typography>
        {solution.cost_estimate?.per_environment?.map((env, index) => (
          <Typography key={index} variant="body1" sx={{ ml: 2, mb: 1 }}>
            • <strong>{env.environment}</strong> ➝ ${env.monthly_usd?.toFixed(2)}
          </Typography>
        ))}
        {solution.cost_estimate?.notes && (
          <Alert severity="info" sx={{ mt: 2 }}>
            📝 Notes: {solution.cost_estimate.notes}
          </Alert>
        )}
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />

      {/* API Spec */}
      {activeSection === SECTIONS.API && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ApiIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             9️⃣ API Specification Stub
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {solution.api_spec_stub || 'No API stub generated.'}
        </Box>
      </Paper>
      )}
      {/* Infrastructure as Code */}
      {activeSection === SECTIONS.IAC && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <CodeIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
            🔟 Infrastructure-as-Code Stub (Terraform/Bicep)
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {solution.infra_as_code_stub || 'No IaC generated.'}
        </Box>
      </Paper>
      )}

      {/* Additional Notes */}
      
      {activeSection === SECTIONS.NOTES && solution.notes && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <NotesIcon sx={{ mr: 1 }} />
            <Typography variant="h6">
              📝 Additional Notes
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {solution.notes}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default SolutionDisplay;
