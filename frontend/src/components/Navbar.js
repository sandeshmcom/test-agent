import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { SmartToy, Home, Add, Assessment } from '@mui/icons-material';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { label: 'Home', path: '/', icon: <Home /> },
    { label: 'Generate', path: '/generate', icon: <Add /> },
    { label: 'Results', path: '/results', icon: <Assessment /> },
  ];

  return (
    <AppBar 
      position="static" 
      sx={{ 
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        color: '#333'
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 3 }}>
          <SmartToy sx={{ mr: 1, color: '#667eea' }} />
          <Typography 
            variant="h6" 
            component="div" 
            className="gradient-text"
            sx={{ fontWeight: 700 }}
          >
            AI Test Agent
          </Typography>
        </Box>
        
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              onClick={() => navigate(item.path)}
              startIcon={item.icon}
              sx={{
                color: location.pathname === item.path ? '#667eea' : '#666',
                fontWeight: location.pathname === item.path ? 600 : 400,
                backgroundColor: location.pathname === item.path ? 'rgba(102, 126, 234, 0.1)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(102, 126, 234, 0.1)',
                },
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;