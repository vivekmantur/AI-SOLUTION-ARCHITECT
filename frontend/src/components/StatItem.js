import React from 'react';
import { Box, Typography } from '@mui/material';

const StatItem = ({ label, value, color = 'blue' }) => {
  const colorClass = `stat-value-${color}`;
  
  return (
    <Box className="stat-item">
      <Typography 
        variant="body2" 
        sx={{ 
          color: '#a0aec0',
          fontSize: '0.9rem'
        }}
      >
        {label}
      </Typography>
      <Typography 
        className={`stat-value ${colorClass}`}
      >
        {value}
      </Typography>
    </Box>
  );
};

export default StatItem;
