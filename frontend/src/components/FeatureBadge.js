import React from 'react';
import { Box } from '@mui/material';

const FeatureBadge = ({ text, color = 'blue' }) => {
  const colorClass = `badge-${color}`;
  
  return (
    <Box 
      component="span"
      className={`feature-badge ${colorClass}`}
    >
      {text}
    </Box>
  );
};

export default FeatureBadge;
