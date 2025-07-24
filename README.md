# AI Test Agent

An intelligent AI-powered tool for generating comprehensive manual test cases from feature requirements. This tool leverages advanced language models (OpenAI GPT or Anthropic Claude) to create detailed, executable test cases that QA teams can use immediately.

## Features

- 🤖 **AI-Powered Generation**: Uses OpenAI GPT or Anthropic Claude to generate intelligent test cases
- 📋 **Comprehensive Test Cases**: Creates detailed manual test cases with step-by-step instructions
- 🎯 **Multiple Test Types**: Supports Functional, UI/UX, Integration, Performance, Security, Usability, Compatibility, and Regression testing
- 📊 **Priority Classification**: Automatically classifies test cases by priority (Critical, High, Medium, Low)
- 📤 **Multiple Export Formats**: Export to JSON, CSV, Markdown, or HTML
- 🎨 **Rich CLI Interface**: Beautiful command-line interface with progress indicators and colored output
- 📁 **File-based Input**: Support for JSON/YAML requirement files for complex projects
- ⚡ **Fast & Efficient**: Async processing for quick test case generation

## Installation

### Prerequisites

- Python 3.8 or higher
- An API key for either OpenAI or Anthropic

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set up API Keys

You need at least one AI provider configured:

#### OpenAI (Recommended)
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

#### Anthropic Claude
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### Optional: Install as Package
```bash
pip install -e .
```

## Quick Start

### 1. Check Available Providers
```bash
python main.py list-providers
```

### 2. Generate Test Cases from Command Line
```bash
python main.py generate \
  --feature "User login functionality" \
  --requirements "Users must be able to log in with email and password" \
  --requirements "System should validate credentials against database" \
  --requirements "Failed login attempts should be logged" \
  --app-type web \
  --test-types Functional \
  --test-types Security
```

### 3. Generate Test Cases from File
```bash
# Create a template file
python main.py create-template

# Edit the requirements_template.json file, then generate
python main.py generate-from-file -i requirements_template.json
```

## Usage Examples

### Basic Command Line Usage

```bash
# Simple test case generation
python main.py generate \
  --feature "Shopping cart checkout process" \
  --requirements "User can add items to cart" \
  --requirements "User can proceed to checkout" \
  --requirements "Payment processing integration" \
  --output-format html \
  --output-file checkout_tests.html
```

### Advanced Usage with Multiple Parameters

```bash
python main.py generate \
  --feature "E-commerce product search and filtering" \
  --requirements "Users can search products by name" \
  --requirements "Users can filter by category, price, rating" \
  --requirements "Search results are paginated" \
  --user-stories "As a customer, I want to find products quickly" \
  --user-stories "As a customer, I want to filter expensive items" \
  --acceptance-criteria "Search should return results within 2 seconds" \
  --acceptance-criteria "Filters should be clearly visible and intuitive" \
  --app-type web \
  --target-audience "Online shoppers, mobile users" \
  --business-context "E-commerce platform serving 100k+ users" \
  --test-types Functional \
  --test-types Performance \
  --test-types Usability \
  --provider openai \
  --output-format markdown \
  --output-file search_test_cases.md
```

### File-based Input Example

Create a `requirements.json` file:

```json
{
  "feature_description": "Multi-factor authentication system",
  "requirements": [
    "Users must enable 2FA through SMS or authenticator app",
    "System should enforce 2FA for admin accounts",
    "Users can disable 2FA with additional verification",
    "2FA codes expire after 5 minutes"
  ],
  "user_stories": [
    "As a security-conscious user, I want to enable 2FA to protect my account",
    "As an admin, I need 2FA to be mandatory for my role"
  ],
  "acceptance_criteria": [
    "Given a user enables 2FA, when they log in, they must provide a second factor",
    "Given an admin account, when created, 2FA should be automatically enabled"
  ],
  "application_type": "web",
  "target_audience": "Business users, administrators",
  "business_context": "Enterprise SaaS platform with security compliance requirements",
  "test_types_requested": ["Functional", "Security", "Usability"]
}
```

Then run:
```bash
python main.py generate-from-file -i requirements.json --output-format html --output-file 2fa_tests.html
```

## Output Formats

### 1. Markdown (Default)
Perfect for documentation and README files. Includes formatted test steps, priorities, and metadata.

### 2. JSON
Structured data format, ideal for integration with test management tools or further processing.

### 3. CSV
Spreadsheet-friendly format for importing into Excel, Google Sheets, or test management systems.

### 4. HTML
Professional-looking report with color-coded priorities and clean formatting for sharing with stakeholders.

## Test Case Structure

Each generated test case includes:

- **Test ID**: Unique identifier (TC_001, TC_002, etc.)
- **Title**: Clear, descriptive test case name
- **Description**: What the test validates
- **Type**: Functional, UI/UX, Integration, Performance, Security, Usability, Compatibility, or Regression
- **Priority**: Critical, High, Medium, or Low
- **Preconditions**: Setup requirements before testing
- **Test Steps**: Detailed step-by-step instructions with expected results
- **Expected Outcome**: Overall expected result
- **Estimated Time**: Time estimate for execution
- **Tags**: Relevant tags for categorization
- **Requirements Covered**: Traceability to original requirements
- **Test Data**: Description of required test data
- **Environment**: Test environment specifications

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `generate` | Generate test cases from command line parameters |
| `generate-from-file` | Generate test cases from a requirements file |
| `list-providers` | Show available AI providers and their status |
| `create-template` | Create a template requirements file |

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--feature, -f` | Feature description (required) | `--feature "User registration"` |
| `--requirements, -r` | Requirements (multiple allowed) | `--requirements "REQ-001: User validation"` |
| `--user-stories, -u` | User stories (multiple allowed) | `--user-stories "As a user, I want..."` |
| `--acceptance-criteria, -a` | Acceptance criteria (multiple) | `--acceptance-criteria "Given... When... Then..."` |
| `--app-type` | Application type | `--app-type web` (web/mobile/desktop/api) |
| `--test-types` | Focus on specific test types | `--test-types Functional --test-types Security` |
| `--provider` | AI provider to use | `--provider openai` (auto/openai/anthropic) |
| `--output-format, -o` | Output format | `--output-format html` (json/csv/markdown/html) |
| `--output-file` | Save to file | `--output-file tests.html` |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | One of OpenAI or Anthropic |
| `ANTHROPIC_API_KEY` | Anthropic API key | One of OpenAI or Anthropic |

## Example Output

Here's what a generated test case looks like:

```markdown
## TC_001: Verify successful user login with valid credentials

**Description:** Validate that users can successfully log in using correct email and password combination

**Type:** Functional | **Priority:** High | **Estimated Time:** 3 minutes

**Preconditions:**
- User account exists in the system
- User knows valid email and password
- Login page is accessible

**Test Steps:**
1. **Action:** Navigate to the login page
   **Expected Result:** Login form is displayed with email and password fields

2. **Action:** Enter valid email address in the email field
   **Expected Result:** Email is accepted and displayed in the field

3. **Action:** Enter valid password in the password field
   **Expected Result:** Password is masked and accepted

4. **Action:** Click the "Login" button
   **Expected Result:** User is redirected to dashboard/home page

**Expected Outcome:** User successfully logs in and is redirected to the appropriate landing page

**Tags:** authentication, login, positive-testing
**Requirements Covered:** REQ-001, REQ-002
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information about your problem
3. Include your Python version, OS, and the exact command you ran

## Roadmap

- [ ] Integration with popular test management tools (TestRail, Jira, Azure DevOps)
- [ ] Support for additional AI providers
- [ ] Web interface for non-technical users
- [ ] Test case versioning and management
- [ ] Automated test data generation
- [ ] Integration with CI/CD pipelines