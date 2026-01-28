import React from 'react';
import {
  Box,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import CloudIcon from '@mui/icons-material/Cloud';

const Sidebar = ({ 
  cloud, 
  setCloud 
}) => {
  return (
    <Box sx={{ p: 2.5, height: '100%', backgroundColor: '#1a202c' }}>
      {/* Configuration Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <SettingsIcon sx={{ color: '#60a5fa', fontSize: 24 }} />
        <Typography 
          variant="h6" 
          sx={{ 
            fontWeight: 600, 
            color: '#e2e8f0',
            fontSize: '1.1rem'
          }}
        >
          Configuration
        </Typography>
      </Box>

      {/* Cloud Selection */}
      <Box sx={{ mb: 3 }}>
        <FormControl 
          fullWidth
          sx={{
            '& .MuiOutlinedInput-root': {
              backgroundColor: '#2d3748',
              '& fieldset': {
                borderColor: '#4a5568',
              },
              '&:hover fieldset': {
                borderColor: '#60a5fa',
              },
              '&.Mui-focused fieldset': {
                borderColor: '#60a5fa',
              },
            },
            '& .MuiInputLabel-root': {
              color: '#a0aec0',
            },
            '& .MuiInputLabel-root.Mui-focused': {
              color: '#60a5fa',
            },
          }}
        >
          <InputLabel id="cloud-select-label">
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CloudIcon sx={{ fontSize: 18 }} />
              Target Cloud
            </Box>
          </InputLabel>
          <Select
            labelId="cloud-select-label"
            value={cloud}
            label="Target Cloud"
            onChange={(e) => setCloud(e.target.value)}
            sx={{ color: '#e2e8f0' }}
          >
            <MenuItem value="azure">🌩️ Azure</MenuItem>
            <MenuItem value="aws">☁️ AWS</MenuItem>
            <MenuItem value="gcp">🌐 GCP</MenuItem>
          </Select>
        </FormControl>
      </Box>
    </Box>
  );
};

export default Sidebar;
