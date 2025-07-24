import React, { useState, useEffect } from 'react';
import {
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  OutlinedInput,
  CircularProgress,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  FormHelperText,
} from '@mui/material';
import { ExpandMore, SmartToy, Add, Remove } from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { 
  generateTestCases, 
  checkProviders, 
  getTestTypes, 
  getApplicationTypes 
} from '../services/api';

const GeneratorPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [providers, setProviders] = useState([]);
  const [testTypes, setTestTypes] = useState([]);
  const [applicationTypes, setApplicationTypes] = useState([]);
  const [requirements, setRequirements] = useState(['']);
  const [userStories, setUserStories] = useState(['']);
  const [acceptanceCriteria, setAcceptanceCriteria] = useState(['']);
  const [integrationPoints, setIntegrationPoints] = useState(['']);

  const { control, handleSubmit, formState: { errors }, watch, setValue } = useForm({
    defaultValues: {
      feature_description: '',
      application_type: 'web',
      target_audience: '',
      business_context: '',
      existing_functionality: '',
      test_types_requested: [],
      provider: 'auto',
    },
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [providersData, testTypesData, appTypesData] = await Promise.all([
          checkProviders(),
          getTestTypes(),
          getApplicationTypes(),
        ]);
        
        setProviders(providersData);
        setTestTypes(testTypesData);
        setApplicationTypes(appTypesData);
      } catch (error) {
        toast.error('Failed to load form data');
      }
    };

    fetchData();
  }, []);

  const handleArrayChange = (index, value, array, setArray) => {
    const newArray = [...array];
    newArray[index] = value;
    setArray(newArray);
  };

  const addArrayItem = (array, setArray) => {
    setArray([...array, '']);
  };

  const removeArrayItem = (index, array, setArray) => {
    if (array.length > 1) {
      const newArray = array.filter((_, i) => i !== index);
      setArray(newArray);
    }
  };

  const onSubmit = async (data) => {
    // Filter out empty requirements and other arrays
    const filteredRequirements = requirements.filter(req => req.trim() !== '');
    const filteredUserStories = userStories.filter(story => story.trim() !== '');
    const filteredAcceptanceCriteria = acceptanceCriteria.filter(criteria => criteria.trim() !== '');
    const filteredIntegrationPoints = integrationPoints.filter(point => point.trim() !== '');

    if (filteredRequirements.length === 0) {
      toast.error('Please add at least one requirement');
      return;
    }

    const requestData = {
      ...data,
      requirements: filteredRequirements,
      user_stories: filteredUserStories.length > 0 ? filteredUserStories : null,
      acceptance_criteria: filteredAcceptanceCriteria.length > 0 ? filteredAcceptanceCriteria : null,
      integration_points: filteredIntegrationPoints.length > 0 ? filteredIntegrationPoints : null,
    };

    setLoading(true);
    try {
      const response = await generateTestCases(requestData);
      
      if (response.success) {
        toast.success(`Generated ${response.test_cases.length} test cases successfully!`);
        // Store results in sessionStorage for the results page
        sessionStorage.setItem('testCaseResults', JSON.stringify(response));
        navigate('/results');
      } else {
        toast.error(response.error || 'Failed to generate test cases');
      }
    } catch (error) {
      toast.error(error.message || 'Failed to generate test cases');
    } finally {
      setLoading(false);
    }
  };

  const availableProviders = providers.filter(p => p.available);
  const hasProviders = availableProviders.length > 0;

  if (!hasProviders && providers.length > 0) {
    return (
      <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
        <CardContent sx={{ textAlign: 'center', p: 4 }}>
          <Typography variant="h5" gutterBottom color="warning.main">
            No AI Providers Configured
          </Typography>
          <Typography variant="body1" color="text.secondary" mb={3}>
            Please configure at least one AI provider to generate test cases.
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            Go Back Home
          </Button>
        </CardContent>
      </Card>
    );
  }

  const ArrayInput = ({ label, array, setArray, placeholder, helperText }) => (
    <Box>
      <Typography variant="subtitle2" gutterBottom fontWeight={600}>
        {label}
      </Typography>
      {array.map((item, index) => (
        <Box key={index} display="flex" gap={1} mb={1}>
          <TextField
            fullWidth
            size="small"
            placeholder={placeholder}
            value={item}
            onChange={(e) => handleArrayChange(index, e.target.value, array, setArray)}
            variant="outlined"
          />
          <Button
            size="small"
            onClick={() => addArrayItem(array, setArray)}
            sx={{ minWidth: 'auto', p: 1 }}
          >
            <Add />
          </Button>
          {array.length > 1 && (
            <Button
              size="small"
              onClick={() => removeArrayItem(index, array, setArray)}
              color="error"
              sx={{ minWidth: 'auto', p: 1 }}
            >
              <Remove />
            </Button>
          )}
        </Box>
      ))}
      {helperText && (
        <FormHelperText sx={{ mt: 1 }}>{helperText}</FormHelperText>
      )}
    </Box>
  );

  return (
    <Box className="fade-in">
      <Typography 
        variant="h4" 
        gutterBottom 
        textAlign="center"
        className="gradient-text"
        sx={{ fontWeight: 700, mb: 4 }}
      >
        Generate Test Cases
      </Typography>

      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>
          {/* Basic Information */}
          <Grid item xs={12}>
            <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom fontWeight={600}>
                  Basic Information
                </Typography>
                
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <Controller
                      name="feature_description"
                      control={control}
                      rules={{ required: 'Feature description is required' }}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label="Feature Description"
                          placeholder="Describe the feature you want to test (e.g., User authentication system)"
                          multiline
                          rows={3}
                          error={!!errors.feature_description}
                          helperText={errors.feature_description?.message}
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Controller
                      name="application_type"
                      control={control}
                      render={({ field }) => (
                        <FormControl fullWidth>
                          <InputLabel>Application Type</InputLabel>
                          <Select {...field} label="Application Type">
                            {applicationTypes.map((type) => (
                              <MenuItem key={type.value} value={type.value}>
                                {type.label}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Controller
                      name="provider"
                      control={control}
                      render={({ field }) => (
                        <FormControl fullWidth>
                          <InputLabel>AI Provider</InputLabel>
                          <Select {...field} label="AI Provider">
                            <MenuItem value="auto">Auto (Best Available)</MenuItem>
                            {availableProviders.map((provider) => (
                              <MenuItem key={provider.name} value={provider.name}>
                                {provider.name.charAt(0).toUpperCase() + provider.name.slice(1)}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Requirements */}
          <Grid item xs={12}>
            <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
              <CardContent sx={{ p: 3 }}>
                <ArrayInput
                  label="Requirements *"
                  array={requirements}
                  setArray={setRequirements}
                  placeholder="Enter a requirement (e.g., Users must be able to log in with email and password)"
                  helperText="Add the functional requirements for your feature. At least one is required."
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Test Configuration */}
          <Grid item xs={12}>
            <Card sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom fontWeight={600}>
                  Test Configuration
                </Typography>
                
                <Controller
                  name="test_types_requested"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Test Types</InputLabel>
                      <Select
                        {...field}
                        multiple
                        input={<OutlinedInput label="Test Types" />}
                        renderValue={(selected) => (
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {selected.map((value) => {
                              const testType = testTypes.find(t => t.value === value);
                              return (
                                <Chip 
                                  key={value} 
                                  label={testType?.label || value} 
                                  size="small" 
                                />
                              );
                            })}
                          </Box>
                        )}
                      >
                        {testTypes.map((type) => (
                          <MenuItem key={type.value} value={type.value}>
                            <Box>
                              <Typography variant="body2" fontWeight={500}>
                                {type.label}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {type.description}
                              </Typography>
                            </Box>
                          </MenuItem>
                        ))}
                      </Select>
                      <FormHelperText>
                        Select specific test types to focus on, or leave empty for comprehensive coverage
                      </FormHelperText>
                    </FormControl>
                  )}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Advanced Options */}
          <Grid item xs={12}>
            <Accordion sx={{ background: 'rgba(255, 255, 255, 0.95)', backdropFilter: 'blur(10px)' }}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6" fontWeight={600}>
                  Advanced Options
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <ArrayInput
                      label="User Stories"
                      array={userStories}
                      setArray={setUserStories}
                      placeholder="As a [user type], I want [goal] so that [benefit]"
                      helperText="Add user stories to provide context for test generation"
                    />
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <ArrayInput
                      label="Acceptance Criteria"
                      array={acceptanceCriteria}
                      setArray={setAcceptanceCriteria}
                      placeholder="Given [context], when [action], then [outcome]"
                      helperText="Add acceptance criteria for more specific test cases"
                    />
                  </Grid>

                  <Grid item xs={12}>
                    <Divider sx={{ my: 2 }} />
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Controller
                      name="target_audience"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label="Target Audience"
                          placeholder="End users, administrators, developers..."
                          helperText="Who will be using this feature?"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Controller
                      name="business_context"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label="Business Context"
                          placeholder="E-commerce platform, healthcare system..."
                          helperText="What type of business/domain is this for?"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12}>
                    <Controller
                      name="existing_functionality"
                      control={control}
                      render={({ field }) => (
                        <TextField
                          {...field}
                          fullWidth
                          label="Existing Functionality"
                          placeholder="Describe related existing features that might interact with this new feature"
                          multiline
                          rows={2}
                          helperText="Help the AI understand how this feature fits into the larger system"
                        />
                      )}
                    />
                  </Grid>

                  <Grid item xs={12}>
                    <ArrayInput
                      label="Integration Points"
                      array={integrationPoints}
                      setArray={setIntegrationPoints}
                      placeholder="External API, Database, Third-party service..."
                      helperText="List systems or services this feature integrates with"
                    />
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>

          {/* Submit Button */}
          <Grid item xs={12}>
            <Box textAlign="center">
              <Button
                type="submit"
                variant="contained"
                size="large"
                disabled={loading || !hasProviders}
                startIcon={loading ? <CircularProgress size={20} /> : <SmartToy />}
                sx={{
                  px: 4,
                  py: 1.5,
                  fontSize: '1.1rem',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a6fd8 0%, #694a91 100%)',
                  },
                }}
              >
                {loading ? 'Generating Test Cases...' : 'Generate Test Cases'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
};

export default GeneratorPage;