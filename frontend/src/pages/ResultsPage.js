import React, { useState, useEffect } from 'react';
import {
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  Box,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
  Divider,
  ButtonGroup,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  ExpandMore,
  GetApp,
  Refresh,
  Assessment,
  AccessTime,
  PlaylistAddCheck,
  Flag,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { exportTestCases } from '../services/api';

const ResultsPage = () => {
  const navigate = useNavigate();
  const [results, setResults] = useState(null);
  const [expandedPanel, setExpandedPanel] = useState(false);

  useEffect(() => {
    const storedResults = sessionStorage.getItem('testCaseResults');
    if (storedResults) {
      setResults(JSON.parse(storedResults));
    } else {
      // No results found, redirect to generator
      navigate('/generate');
    }
  }, [navigate]);

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedPanel(isExpanded ? panel : false);
  };

  const handleExport = async (format) => {
    try {
      await exportTestCases(format);
      toast.success(`Test cases exported as ${format.toUpperCase()}`);
    } catch (error) {
      toast.error(error.message);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return '#f44336';
      case 'high':
        return '#ff9800';
      case 'medium':
        return '#2196f3';
      case 'low':
        return '#4caf50';
      default:
        return '#9e9e9e';
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      'Functional': '#2196f3',
      'UI/UX': '#9c27b0',
      'Integration': '#ff9800',
      'Security': '#f44336',
      'Performance': '#4caf50',
      'Usability': '#00bcd4',
      'Compatibility': '#795548',
      'Regression': '#607d8b',
    };
    return colors[type] || '#9e9e9e';
  };

  if (!results) {
    return (
      <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
        <CardContent sx={{ textAlign: 'center', p: 4 }}>
          <Typography variant="h5" gutterBottom>
            No Test Results Found
          </Typography>
          <Typography variant="body1" color="text.secondary" mb={3}>
            Please generate test cases first.
          </Typography>
          <Button variant="contained" onClick={() => navigate('/generate')}>
            Generate Test Cases
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!results.success) {
    return (
      <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
        <CardContent sx={{ textAlign: 'center', p: 4 }}>
          <Typography variant="h5" gutterBottom color="error">
            Generation Failed
          </Typography>
          <Typography variant="body1" color="text.secondary" mb={3}>
            {results.error || 'An error occurred while generating test cases.'}
          </Typography>
          <Button variant="contained" onClick={() => navigate('/generate')}>
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  const { test_cases, summary, generation_time, provider_used } = results;

  return (
    <Box className="fade-in">
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography 
          variant="h4" 
          className="gradient-text"
          sx={{ fontWeight: 700 }}
        >
          Generated Test Cases
        </Typography>
        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={() => navigate('/generate')}
          >
            Generate New
          </Button>
          <ButtonGroup variant="contained">
            <Button
              onClick={() => handleExport('json')}
              startIcon={<GetApp />}
              className="export-button"
            >
              JSON
            </Button>
            <Button
              onClick={() => handleExport('csv')}
              startIcon={<GetApp />}
              className="export-button"
            >
              CSV
            </Button>
            <Button
              onClick={() => handleExport('markdown')}
              startIcon={<GetApp />}
              className="export-button"
            >
              Markdown
            </Button>
            <Button
              onClick={() => handleExport('html')}
              startIcon={<GetApp />}
              className="export-button"
            >
              HTML
            </Button>
          </ButtonGroup>
        </Box>
      </Box>

      {/* Summary */}
      <Card 
        sx={{ 
          background: 'rgba(255, 255, 255, 0.95)', 
          backdropFilter: 'blur(10px)',
          mb: 4 
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom fontWeight={600}>
            Generation Summary
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center">
                <Assessment sx={{ fontSize: 40, color: '#667eea', mb: 1 }} />
                <Typography variant="h4" fontWeight={700} color="#667eea">
                  {summary.total}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Test Cases
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center">
                <AccessTime sx={{ fontSize: 40, color: '#764ba2', mb: 1 }} />
                <Typography variant="h4" fontWeight={700} color="#764ba2">
                  {generation_time.toFixed(1)}s
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Generation Time
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center">
                <PlaylistAddCheck sx={{ fontSize: 40, color: '#4caf50', mb: 1 }} />
                <Typography variant="h4" fontWeight={700} color="#4caf50">
                  {summary.estimated_total_time?.split(' ')[0] || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Estimated Minutes
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Box textAlign="center">
                <Flag sx={{ fontSize: 40, color: '#ff9800', mb: 1 }} />
                <Typography variant="h4" fontWeight={700} color="#ff9800">
                  {provider_used}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  AI Provider
                </Typography>
              </Box>
            </Grid>
          </Grid>

          {/* Summary Tables */}
          <Grid container spacing={3} mt={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" fontWeight={600} mb={2}>
                By Test Type
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Type</TableCell>
                      <TableCell align="right">Count</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(summary.by_type || {}).map(([type, count]) => (
                      <TableRow key={type}>
                        <TableCell>
                          <Chip
                            label={type}
                            size="small"
                            sx={{
                              backgroundColor: `${getTypeColor(type)}15`,
                              color: getTypeColor(type),
                            }}
                          />
                        </TableCell>
                        <TableCell align="right">{count}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" fontWeight={600} mb={2}>
                By Priority
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Priority</TableCell>
                      <TableCell align="right">Count</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(summary.by_priority || {}).map(([priority, count]) => (
                      <TableRow key={priority}>
                        <TableCell>
                          <Chip
                            label={priority}
                            size="small"
                            sx={{
                              backgroundColor: `${getPriorityColor(priority)}15`,
                              color: getPriorityColor(priority),
                            }}
                          />
                        </TableCell>
                        <TableCell align="right">{count}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Test Cases */}
      <Typography variant="h5" gutterBottom fontWeight={600} mb={3}>
        Test Cases ({test_cases.length})
      </Typography>

      {test_cases.map((testCase, index) => (
        <Accordion
          key={testCase.test_id}
          expanded={expandedPanel === testCase.test_id}
          onChange={handleAccordionChange(testCase.test_id)}
          sx={{ 
            mb: 2,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            border: `2px solid ${getPriorityColor(testCase.priority)}15`,
            borderLeft: `4px solid ${getPriorityColor(testCase.priority)}`,
            '&:before': {
              display: 'none',
            },
          }}
          className="test-case-card"
        >
          <AccordionSummary
            expandIcon={<ExpandMore />}
            sx={{ px: 3, py: 2 }}
          >
            <Box sx={{ width: '100%' }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="h6" fontWeight={600}>
                  {testCase.test_id}: {testCase.title}
                </Typography>
                <Box display="flex" gap={1}>
                  <Chip
                    label={testCase.priority}
                    size="small"
                    sx={{
                      backgroundColor: `${getPriorityColor(testCase.priority)}15`,
                      color: getPriorityColor(testCase.priority),
                      fontWeight: 600,
                    }}
                  />
                  <Chip
                    label={testCase.test_type}
                    size="small"
                    sx={{
                      backgroundColor: `${getTypeColor(testCase.test_type)}15`,
                      color: getTypeColor(testCase.test_type),
                    }}
                  />
                  <Chip
                    label={testCase.estimated_time}
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">
                {testCase.description}
              </Typography>
            </Box>
          </AccordionSummary>

          <AccordionDetails sx={{ px: 3, py: 2, pt: 0 }}>
            <Grid container spacing={3}>
              {/* Preconditions */}
              {testCase.preconditions && testCase.preconditions.length > 0 && (
                <Grid item xs={12}>
                  <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                    Preconditions
                  </Typography>
                  <Box component="ul" sx={{ pl: 2, m: 0 }}>
                    {testCase.preconditions.map((precondition, idx) => (
                      <Typography 
                        key={idx} 
                        component="li" 
                        variant="body2" 
                        sx={{ mb: 0.5 }}
                      >
                        {precondition}
                      </Typography>
                    ))}
                  </Box>
                </Grid>
              )}

              {/* Test Steps */}
              <Grid item xs={12}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Test Steps
                </Typography>
                {testCase.test_steps.map((step, stepIndex) => (
                  <Box 
                    key={stepIndex}
                    sx={{ 
                      mb: 2, 
                      p: 2, 
                      border: '1px solid #e0e0e0', 
                      borderRadius: 2,
                      backgroundColor: '#fafafa',
                    }}
                  >
                    <Box display="flex" alignItems="flex-start" gap={2}>
                      <Box className="step-number">
                        {step.step_number}
                      </Box>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="body2" fontWeight={500} mb={1}>
                          <strong>Action:</strong> {step.action}
                        </Typography>
                        <Typography variant="body2" color="success.main" mb={1}>
                          <strong>Expected Result:</strong> {step.expected_result}
                        </Typography>
                        {step.notes && (
                          <Typography variant="caption" color="text.secondary" fontStyle="italic">
                            <strong>Notes:</strong> {step.notes}
                          </Typography>
                        )}
                      </Box>
                    </Box>
                  </Box>
                ))}
              </Grid>

              {/* Expected Outcome */}
              <Grid item xs={12}>
                <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                  Expected Outcome
                </Typography>
                <Alert severity="success" sx={{ mb: 2 }}>
                  {testCase.expected_outcome}
                </Alert>
              </Grid>

              {/* Additional Info */}
              <Grid item xs={12}>
                <Grid container spacing={2}>
                  {testCase.tags && testCase.tags.length > 0 && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Tags
                      </Typography>
                      <Box display="flex" flexWrap="wrap" gap={0.5}>
                        {testCase.tags.map((tag, idx) => (
                          <Chip key={idx} label={tag} size="small" variant="outlined" />
                        ))}
                      </Box>
                    </Grid>
                  )}

                  {testCase.requirements_covered && testCase.requirements_covered.length > 0 && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Requirements Covered
                      </Typography>
                      <Box component="ul" sx={{ pl: 2, m: 0 }}>
                        {testCase.requirements_covered.map((req, idx) => (
                          <Typography 
                            key={idx} 
                            component="li" 
                            variant="body2" 
                            sx={{ mb: 0.5 }}
                          >
                            {req}
                          </Typography>
                        ))}
                      </Box>
                    </Grid>
                  )}

                  {testCase.test_data_needed && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Test Data Needed
                      </Typography>
                      <Typography variant="body2">
                        {testCase.test_data_needed}
                      </Typography>
                    </Grid>
                  )}

                  {testCase.environment && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Environment Requirements
                      </Typography>
                      <Typography variant="body2">
                        {testCase.environment}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>
      ))}

      {/* Bottom Actions */}
      <Box textAlign="center" mt={4}>
        <Button
          variant="outlined"
          onClick={() => navigate('/generate')}
          sx={{ mr: 2 }}
        >
          Generate More Test Cases
        </Button>
      </Box>
    </Box>
  );
};

export default ResultsPage;