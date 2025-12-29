import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import SearchIcon from '@mui/icons-material/Search';
import BoltIcon from '@mui/icons-material/Bolt';
import LinkIcon from '@mui/icons-material/Link';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import FeatureBadge from './FeatureBadge';
import ActionButton from './ActionButton';

const Dashboard = () => {
  const handleActionClick = (action) => {
    console.log(`Action clicked: ${action}`);
    // Add your action handlers here
  };

  return (
    <Box>
      {/* Welcome Section */}
      <Paper 
        elevation={0}
        sx={{ 
          p: 4, 
          mb: 3,
          backgroundColor: '#2d3748',
          borderRadius: 2,
          border: '1px solid #4a5568'
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 3 }}>
          <Box
            sx={{
              width: 64,
              height: 64,
              borderRadius: 2,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}
          >
            <SmartToyIcon sx={{ fontSize: 36, color: 'white' }} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography 
              variant="h4" 
              sx={{ 
                fontWeight: 700, 
                color: '#e2e8f0',
                mb: 1.5
              }}
            >
              Welcome to AI DevOps Assistant
            </Typography>
            <Typography 
              variant="body1" 
              sx={{ 
                color: '#a0aec0',
                mb: 2.5,
                lineHeight: 1.6
              }}
            >
              Your intelligent companion for automated code analysis, bug fixing, and pull request management. 
              Powered by Ollama CodeLlama and integrated with Azure DevOps.
            </Typography>
            <Box>
              <FeatureBadge text="Azure DevOps Integration" color="blue" />
              <FeatureBadge text="AI-Powered Analysis" color="green" />
              <FeatureBadge text="Automated PR Creation" color="orange" />
            </Box>
          </Box>
        </Box>
      </Paper>

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Chat Section */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0}
            sx={{ 
              p: 3, 
              backgroundColor: '#2d3748',
              borderRadius: 2,
              border: '1px solid #4a5568',
              height: '100%'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <ChatBubbleOutlineIcon sx={{ fontSize: 32, color: '#60a5fa' }} />
              <Box>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    fontWeight: 600, 
                    color: '#e2e8f0'
                  }}
                >
                  Chat
                </Typography>
                <Typography 
                  variant="body2" 
                  sx={{ 
                    color: '#718096',
                    fontWeight: 500
                  }}
                >
                  Chat Interface
                </Typography>
              </Box>
            </Box>
            <Typography 
              variant="body2" 
              sx={{ 
                color: '#a0aec0',
                lineHeight: 1.6
              }}
            >
              Interact with AI to analyze bugs, get code suggestions, and automate fixes.
            </Typography>
          </Paper>
        </Grid>

        {/* Code Analysis Section */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0}
            sx={{ 
              p: 3, 
              backgroundColor: '#2d3748',
              borderRadius: 2,
              border: '1px solid #4a5568',
              height: '100%'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <SearchIcon sx={{ fontSize: 32, color: '#a78bfa' }} />
              <Box>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    fontWeight: 600, 
                    color: '#e2e8f0'
                  }}
                >
                  Code Analysis
                </Typography>
              </Box>
            </Box>
            <Typography 
              variant="body2" 
              sx={{ 
                color: '#a0aec0',
                lineHeight: 1.6
              }}
            >
              Upload error images or describe bugs. AI finds and fixes code automatically.
            </Typography>
          </Paper>
        </Grid>

        {/* Quick Actions Section */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0}
            sx={{ 
              p: 3, 
              backgroundColor: '#2d3748',
              borderRadius: 2,
              border: '1px solid #4a5568'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <BoltIcon sx={{ fontSize: 28, color: '#fbbf24' }} />
              <Typography 
                variant="h6" 
                sx={{ 
                  fontWeight: 600, 
                  color: '#e2e8f0'
                }}
              >
                Quick Actions
              </Typography>
            </Box>
            <Typography 
              variant="body2" 
              sx={{ 
                color: '#a0aec0',
                mb: 2.5,
                lineHeight: 1.6
              }}
            >
              Fast access to common tasks and useful shortcuts
            </Typography>
            <Box>
              <ActionButton 
                icon={LinkIcon}
                text="Open in Azure DevOps"
                onClick={() => handleActionClick('azure-devops')}
              />
              <ActionButton 
                icon={HealthAndSafetyIcon}
                text="Check AI Service"
                onClick={() => handleActionClick('check-service')}
              />
              <ActionButton 
                icon={MenuBookIcon}
                text="View Documentation"
                onClick={() => handleActionClick('documentation')}
              />
              <ActionButton 
                icon={RestartAltIcon}
                text="Reset Statistics"
                onClick={() => handleActionClick('reset-stats')}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Multi-Repo Support Section */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0}
            sx={{ 
              p: 3, 
              backgroundColor: '#2d3748',
              borderRadius: 2,
              border: '1px solid #4a5568'
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <AccountTreeIcon sx={{ fontSize: 32, color: '#68d391' }} />
              <Box>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    fontWeight: 600, 
                    color: '#e2e8f0'
                  }}
                >
                  Repo
                </Typography>
                <Typography 
                  variant="body2" 
                  sx={{ 
                    color: '#718096',
                    fontWeight: 500
                  }}
                >
                  Multi-Repo Support
                </Typography>
              </Box>
            </Box>
            <Typography 
              variant="body2" 
              sx={{ 
                color: '#a0aec0',
                lineHeight: 1.6
              }}
            >
              Connect and manage multiple Azure DevOps repositories from one interface.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
