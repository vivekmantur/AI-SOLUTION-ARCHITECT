import React from 'react';
import { Box, Typography, IconButton } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';

const RepositoryCard = ({ name, path, onDelete }) => {
  return (
    <Box className="repo-card">
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flex: 1 }}>
        <CheckCircleIcon sx={{ color: '#48bb78', fontSize: 20 }} />
        <Box>
          <Typography 
            variant="body1" 
            sx={{ 
              fontWeight: 600, 
              color: '#e2e8f0',
              fontSize: '0.95rem'
            }}
          >
            {name}
          </Typography>
          <Typography 
            variant="caption" 
            sx={{ 
              color: '#a0aec0',
              fontSize: '0.75rem'
            }}
          >
            {path}
          </Typography>
        </Box>
      </Box>
      <IconButton 
        size="small" 
        onClick={onDelete}
        sx={{ 
          color: '#fc8181',
          '&:hover': {
            backgroundColor: 'rgba(252, 129, 129, 0.1)'
          }
        }}
      >
        <DeleteOutlineIcon fontSize="small" />
      </IconButton>
    </Box>
  );
};

export default RepositoryCard;
