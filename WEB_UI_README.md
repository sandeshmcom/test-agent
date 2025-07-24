# AI Test Agent Web UI

A beautiful, modern web interface for the AI Test Agent, built with React and Material-UI. Generate comprehensive manual test cases through an intuitive graphical interface.

## 🌟 Features

- **🎨 Modern UI**: Beautiful, responsive design with Material-UI components
- **📱 Mobile Friendly**: Works seamlessly on desktop, tablet, and mobile devices
- **🚀 Real-time Generation**: Live progress indicators during test case generation
- **📊 Visual Summary**: Rich dashboards with charts and statistics
- **💾 Multiple Export Formats**: Download test cases as JSON, CSV, Markdown, or HTML
- **🔄 Provider Selection**: Choose between OpenAI and Anthropic AI providers
- **📝 Advanced Form**: Comprehensive form with dynamic field management
- **🎯 Priority Color Coding**: Visual priority indicators for easy scanning
- **📁 Session Management**: Automatic result storage and navigation

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern, high-performance Python web framework
- **Async Support**: Non-blocking operations for better performance
- **OpenAPI Integration**: Automatic API documentation
- **CORS Enabled**: Cross-origin requests for frontend integration
- **File Export**: Direct download support for all export formats

### Frontend (React)
- **React 18**: Latest React features with hooks and context
- **Material-UI**: Google's Material Design components
- **React Router**: Client-side routing for SPA experience
- **React Hook Form**: Efficient form management with validation
- **Axios**: HTTP client for API communication
- **React Hot Toast**: Beautiful notification system

## 📦 Quick Start

### Prerequisites

- **Python 3.8+**: For backend server
- **Node.js 16+**: For frontend development
- **AI Provider API Key**: OpenAI or Anthropic

### 🚀 Easy Start (Recommended)

```bash
# Start both backend and frontend automatically
./start_ui.sh
```

This script will:
- Check dependencies
- Install packages
- Start backend on port 8000
- Start frontend on port 3000
- Open both in separate terminals or tmux panes

### 🔧 Manual Start

#### Terminal 1 - Backend
```bash
./start_backend.sh
```

#### Terminal 2 - Frontend
```bash
./start_frontend.sh
```

### 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 User Guide

### 1. Home Page
- **Provider Status**: Check if AI providers are configured
- **Feature Overview**: Learn about available test types
- **Quick Navigation**: Jump to test generation

### 2. Generate Test Cases

#### Basic Information
- **Feature Description**: Describe what you want to test
- **Application Type**: Web, Mobile, Desktop, or API
- **AI Provider**: Choose your preferred AI model

#### Requirements (Required)
- Add functional requirements one by one
- Use the `+` button to add more requirements
- At least one requirement is mandatory

#### Test Configuration
- **Test Types**: Select specific types or leave empty for comprehensive coverage
  - Functional, UI/UX, Integration, Performance
  - Security, Usability, Compatibility, Regression

#### Advanced Options (Optional)
- **User Stories**: Add user perspective stories
- **Acceptance Criteria**: Define success conditions
- **Target Audience**: Specify who uses the feature
- **Business Context**: Provide domain context
- **Existing Functionality**: Describe related features
- **Integration Points**: List external dependencies

### 3. Results Page

#### Summary Dashboard
- **Test Case Count**: Total generated test cases
- **Generation Time**: How long it took to generate
- **Estimated Time**: Total time to execute all tests
- **AI Provider**: Which model was used

#### Test Case Details
- **Priority Color Coding**: Visual priority indicators
  - 🔴 Critical, 🟠 High, 🔵 Medium, 🟢 Low
- **Expandable Cards**: Click to view full test details
- **Step-by-step Instructions**: Clear, numbered test steps
- **Expected Results**: Detailed expected outcomes

#### Export Options
- **JSON**: Structured data for tools integration
- **CSV**: Spreadsheet format for Excel/Google Sheets
- **Markdown**: Documentation-friendly format
- **HTML**: Professional reports for stakeholders

## 🛠️ Development

### Backend Development

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### API Development

The backend provides a REST API with the following endpoints:

- `GET /providers` - Check available AI providers
- `POST /generate` - Generate test cases
- `GET /export/{format}` - Export test cases
- `GET /test-types` - Get available test types
- `GET /application-types` - Get application types

Full API documentation is available at http://localhost:8000/docs

## 🎨 UI Components

### Key Components

- **Navbar**: Main navigation with current page highlighting
- **HomePage**: Welcome page with provider status
- **GeneratorPage**: Comprehensive form for test generation
- **ResultsPage**: Results display with export functionality
- **ArrayInput**: Dynamic field management for lists
- **TestCaseCard**: Individual test case display

### Styling

- **Material-UI Theme**: Custom theme with brand colors
- **Gradient Backgrounds**: Beautiful gradient overlays
- **Glass Morphism**: Modern translucent card effects
- **Responsive Design**: Mobile-first approach
- **Color Coding**: Priority and type-based color schemes

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Customization

#### Theme Customization
Edit `frontend/src/index.js` to modify the Material-UI theme:
- Colors
- Typography
- Component styles
- Border radius

#### API Configuration
Edit `frontend/src/services/api.js` to modify:
- Base URL
- Timeout settings
- Request/response interceptors

## 🚀 Deployment

### Backend Deployment

```bash
# Install production dependencies
pip install uvicorn[standard] gunicorn

# Start with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Serve static files
# Deploy build/ folder to your web server
```

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
- Check Python version (3.8+)
- Verify API keys are set
- Check port 8000 availability

#### Frontend Won't Start
- Check Node.js version (16+)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall

#### CORS Issues
- Ensure backend CORS is configured for frontend URL
- Check frontend proxy configuration

#### Generation Fails
- Verify API keys are valid
- Check internet connection
- Review backend logs for errors

### Performance Tips

#### Backend
- Use async/await for API calls
- Implement request caching
- Add request rate limiting

#### Frontend
- Use React.memo for expensive components
- Implement virtual scrolling for large lists
- Optimize bundle size with code splitting

## 🎯 Best Practices

### Test Generation
- **Be Specific**: Provide detailed feature descriptions
- **Add Context**: Include business context and user stories
- **Choose Types**: Select relevant test types for better focus
- **Review Results**: Always review generated tests before use

### UI Usage
- **Save Progress**: Use export to save your work
- **Multiple Sessions**: Generate different test suites separately
- **Review Summaries**: Check the summary before diving into details
- **Share Results**: Use HTML export for stakeholder reviews

## 📈 Future Enhancements

### Planned Features
- **Test Management**: Save and organize test suites
- **Collaboration**: Team sharing and comments
- **Integration**: Direct export to test management tools
- **Templates**: Reusable test generation templates
- **Analytics**: Usage statistics and insights

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License. See the main README.md for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs or request features
- **Documentation**: Check the main README.md
- **Community**: Join discussions and share feedback