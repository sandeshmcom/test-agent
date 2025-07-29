# Flask OpenAI Test Generator API

A Flask API that generates Playwright test scripts using OpenAI's GPT-4 model.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   Edit `app.py` and replace `"sk-xxxxxxxxxxxxxxxx"` with your actual OpenAI API key.

3. **Start the Flask server:**
   ```bash
   python app.py
   ```
   The server will run on `http://localhost:5001`

## Usage

### Method 1: Interactive Client
Run the interactive client:
```bash
python client.py
```
Then enter prompts interactively.

### Method 2: Command Line
Pass the prompt as command line arguments:
```bash
python client.py "Write a Playwright test for login functionality"
```

### Method 3: Example Script
Run the example with a predefined prompt:
```bash
python example.py
```

### Method 4: Direct API Call
You can also call the API directly using curl:
```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Playwright test for button click"}'
```

## Files

- `app.py` - Flask server with OpenAI integration
- `client.py` - Interactive client to call the API
- `example.py` - Example script with sample prompt
- `requirements.txt` - Python dependencies

## API Endpoint

**POST** `/generate`

**Request Body:**
```json
{
  "prompt": "Your test generation prompt here"
}
```

**Response:**
```json
{
  "code": "Generated Playwright test code"
}
```