import React from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  CircularProgress,
} from '@mui/material';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import DescriptionIcon from '@mui/icons-material/Description';

const DEFAULT_REQUIREMENTS = `We need a multi-tenant SaaS platform where enterprise clients can upload CSV and Excel files,
validate data, store securely, and view analytics dashboards. Must support Azure AD SSO, audit logging,
API-based ingestion, row-level security, and scale to 10,000 users globally. Deploy on Azure with 99.9%
availability and GDPR compliance. Go-live in 3 months.`;

const RequirementsInput = ({ 
  requirements, 
  setRequirements, 
  onGenerate, 
  loading 
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <DescriptionIcon sx={{ mr: 1 }} />
        <Typography variant="h6">
          1️⃣ Enter Business / Technical Requirements
        </Typography>
      </Box>

      <TextField
        fullWidth
        multiline
        rows={10}
        value={requirements}
        onChange={(e) => setRequirements(e.target.value)}
        placeholder="Paste or type requirements here..."
        variant="outlined"
        sx={{ mb: 2 }}
      />

      <Button
        variant="contained"
        size="large"
        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RocketLaunchIcon />}
        onClick={onGenerate}
        disabled={loading || !requirements.trim()}
        fullWidth
        sx={{ 
          py: 1.5,
          fontSize: '1.1rem',
        }}
      >
        {loading ? 'AI Architect is designing your solution...' : 'Generate Solution Design'}
      </Button>
    </Box>
  );
};

export default RequirementsInput;
export { DEFAULT_REQUIREMENTS };
