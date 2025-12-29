import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Drawer,
  AppBar,
  Toolbar,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import ArchitectureIcon from '@mui/icons-material/Architecture';
import Sidebar from './components/Sidebar';
import RequirementsInput, { DEFAULT_REQUIREMENTS } from './components/RequirementsInput';
import SolutionDisplay from './components/SolutionDisplay';
import { healthCheck, generateDesign } from './services/api';
import './App.css';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3b82f6',
    },
    secondary: {
      main: '#8b5cf6',
    },
    background: {
      default: '#1a202c',
      paper: '#2d3748',
    },
    text: {
      primary: '#e2e8f0',
      secondary: '#a0aec0',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#1a202c',
          color: '#e2e8f0',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

const DRAWER_WIDTH = 360;

function App() {
  const [cloud, setCloud] = useState('azure');
  const [detailLevel, setDetailLevel] = useState('high');
  const [requirements, setRequirements] = useState(DEFAULT_REQUIREMENTS);
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(false);
  const [healthStatus, setHealthStatus] = useState(null);

  const handleHealthCheck = async () => {
    const result = await healthCheck();
    setHealthStatus(result);
  };

  const handleGenerate = async () => {
    setLoading(true);
    setSolution(null);
    
    try {
      const result = await generateDesign(requirements, cloud, detailLevel);
      
      if (result.success) {
        setSolution(result.data.solution);
      } else {
        // Show error in console or you could add error state
        console.error('Error generating design:', result.error);
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error('Unexpected error:', error);
      alert('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        {/* App Bar */}
        <AppBar 
          position="fixed" 
          elevation={0}
          sx={{ 
            zIndex: (theme) => theme.zIndex.drawer + 1,
            backgroundColor: '#2d3748',
            borderBottom: '1px solid #4a5568',
          }}
        >
          <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: 1,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <ArchitectureIcon sx={{ fontSize: 24, color: 'white' }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700, lineHeight: 1.2 }}>
                  🧠 AI Solution Architect
                </Typography>
                <Typography variant="caption" sx={{ color: '#a0aec0' }}>
                  Generate Cloud Architecture from Business Requirements using AI
                </Typography>
              </Box>
            </Box>
          </Toolbar>
        </AppBar>

        {/* Sidebar */}
        <Drawer
          variant="permanent"
          sx={{
            width: DRAWER_WIDTH,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: DRAWER_WIDTH,
              boxSizing: 'border-box',
              mt: '64px',
              backgroundColor: '#1a202c',
              borderRight: '1px solid #2d3748',
            },
          }}
        >
          <Sidebar 
            cloud={cloud}
            setCloud={setCloud}
            detailLevel={detailLevel}
            setDetailLevel={setDetailLevel}
            onHealthCheck={handleHealthCheck}
            healthStatus={healthStatus}
          />
        </Drawer>

        {/* Main Content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 4,
            mt: '64px',
            backgroundColor: '#1a202c',
            minHeight: 'calc(100vh - 64px)',
          }}
        >
          <Container maxWidth="xl">
            <RequirementsInput
              requirements={requirements}
              setRequirements={setRequirements}
              onGenerate={handleGenerate}
              loading={loading}
            />
            
            {solution && <SolutionDisplay solution={solution} />}
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
