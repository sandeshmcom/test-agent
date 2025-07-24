import React, { useState, useEffect } from 'react';
import {
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  Box,
  Chip,
  Container,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  SmartToy,
  Speed,
  GetApp,
  Security,
  Integration,
  BugReport,
  Visibility,
  DeviceHub,
  CheckCircle,
  Warning,
} from '@mui/icons-material';
import toast from 'react-hot-toast';
import { checkProviders } from '../services/api';

const HomePage = () => {
  const navigate = useNavigate();
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const data = await checkProviders();
        setProviders(data);
      } catch (error) {
        toast.error('Failed to check AI providers');
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, []);

  const features = [
    {
      icon: <SmartToy sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'AI-Powered Generation',
      description: 'Uses advanced language models to create comprehensive test cases',
    },
    {
      icon: <Speed sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'Fast & Efficient',
      description: 'Generate dozens of test cases in seconds, not hours',
    },
    {
      icon: <GetApp sx={{ fontSize: 40, color: '#667eea' }} />,
      title: 'Multiple Export Formats',
      description: 'Export to JSON, CSV, Markdown, or HTML formats',
    },
  ];

  const testTypes = [
    { label: 'Functional', icon: <BugReport />, color: '#2196f3' },
    { label: 'UI/UX', icon: <Visibility />, color: '#9c27b0' },
    { label: 'Integration', icon: <DeviceHub />, color: '#ff9800' },
    { label: 'Security', icon: <Security />, color: '#f44336' },
    { label: 'Performance', icon: <Speed />, color: '#4caf50' },
    { label: 'Usability', icon: <Visibility />, color: '#00bcd4' },
  ];

  const availableProviders = providers.filter(p => p.available);
  const hasProviders = availableProviders.length > 0;

  return (
    <Container maxWidth="lg">
      <Box className="fade-in">
        {/* Hero Section */}
        <Box textAlign="center" mb={6}>
          <Typography 
            variant="h3" 
            component="h1" 
            gutterBottom
            className="gradient-text"
            sx={{ fontWeight: 700, mb: 2 }}
          >
            AI Test Agent
          </Typography>
          <Typography 
            variant="h6" 
            color="rgba(255, 255, 255, 0.9)" 
            gutterBottom
            sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}
          >
            Generate comprehensive manual test cases from your requirements using advanced AI. 
            Save time, improve coverage, and ensure quality.
          </Typography>
          
          {/* Provider Status */}
          <Box mb={4}>
            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center" gap={2}>
                <CircularProgress size={20} sx={{ color: 'white' }} />
                <Typography color="rgba(255, 255, 255, 0.8)">
                  Checking AI providers...
                </Typography>
              </Box>
            ) : hasProviders ? (
              <Alert 
                severity="success" 
                sx={{ 
                  backgroundColor: 'rgba(76, 175, 80, 0.1)', 
                  color: 'white',
                  border: '1px solid rgba(76, 175, 80, 0.3)',
                  maxWidth: 400,
                  mx: 'auto'
                }}
                icon={<CheckCircle sx={{ color: '#4caf50' }} />}
              >
                AI providers configured and ready
              </Alert>
            ) : (
              <Alert 
                severity="warning"
                sx={{ 
                  backgroundColor: 'rgba(255, 152, 0, 0.1)', 
                  color: 'white',
                  border: '1px solid rgba(255, 152, 0, 0.3)',
                  maxWidth: 400,
                  mx: 'auto'
                }}
                icon={<Warning sx={{ color: '#ff9800' }} />}
              >
                No AI providers configured. Please set up API keys.
              </Alert>
            )}
          </Box>

          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/generate')}
            disabled={!hasProviders}
            sx={{
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              background: hasProviders 
                ? 'linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%)'
                : 'rgba(255, 255, 255, 0.1)',
              color: 'white',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              '&:hover': {
                background: hasProviders 
                  ? 'linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.2) 100%)'
                  : 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            {hasProviders ? 'Start Generating Tests' : 'Configure AI Provider First'}
          </Button>
        </Box>

        {/* Features Section */}
        <Grid container spacing={4} mb={6}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  }
                }}
              >
                <CardContent sx={{ textAlign: 'center', p: 3 }}>
                  <Box mb={2}>{feature.icon}</Box>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Test Types Section */}
        <Card 
          sx={{ 
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            mb: 4
          }}
        >
          <CardContent sx={{ p: 4 }}>
            <Typography 
              variant="h5" 
              gutterBottom 
              textAlign="center"
              fontWeight={600}
              mb={3}
            >
              Supported Test Types
            </Typography>
            <Grid container spacing={2} justifyContent="center">
              {testTypes.map((type, index) => (
                <Grid item key={index}>
                  <Chip
                    icon={type.icon}
                    label={type.label}
                    sx={{
                      backgroundColor: `${type.color}15`,
                      color: type.color,
                      fontWeight: 500,
                      '& .MuiChip-icon': {
                        color: type.color,
                      },
                    }}
                  />
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>

        {/* Provider Status Details */}
        {!loading && (
          <Card 
            sx={{ 
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
            }}
          >
            <CardContent sx={{ p: 4 }}>
              <Typography 
                variant="h6" 
                gutterBottom 
                fontWeight={600}
                mb={3}
              >
                AI Provider Status
              </Typography>
              <Grid container spacing={2}>
                {providers.map((provider) => (
                  <Grid item xs={12} sm={6} key={provider.name}>
                    <Box 
                      display="flex" 
                      alignItems="center" 
                      gap={2}
                      p={2}
                      border={1}
                      borderColor={provider.available ? 'success.main' : 'grey.300'}
                      borderRadius={2}
                      backgroundColor={provider.available ? 'rgba(76, 175, 80, 0.05)' : 'rgba(0, 0, 0, 0.02)'}
                    >
                      {provider.available ? (
                        <CheckCircle sx={{ color: 'success.main' }} />
                      ) : (
                        <Warning sx={{ color: 'warning.main' }} />
                      )}
                      <Box>
                        <Typography variant="subtitle1" fontWeight={500}>
                          {provider.name.charAt(0).toUpperCase() + provider.name.slice(1)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {provider.description}
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  );
};

export default HomePage;