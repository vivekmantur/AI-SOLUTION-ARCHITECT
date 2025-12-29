import React from 'react';
import { Box } from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const ActionButton = ({ icon: Icon, text, onClick }) => {
  return (
    <Box 
      className="action-button"
      onClick={onClick}
      component="button"
    >
      <Box className="action-button-content">
        <Icon sx={{ fontSize: 20, color: '#60a5fa' }} />
        <span>{text}</span>
      </Box>
      <ArrowForwardIcon sx={{ fontSize: 18, color: '#718096' }} />
    </Box>
  );
};

export default ActionButton;
