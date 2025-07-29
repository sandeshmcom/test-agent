#!/usr/bin/env python3
"""
Example script demonstrating how to call the Flask API.
"""

import requests
import json

def example_api_call():
    """Example of calling the Flask API with a sample prompt."""
    
    # API endpoint
    url = "http://localhost:5001/generate"
    
    # Sample prompt for generating a Playwright test
    sample_prompt = "Write a Playwright test that logs into a website with username 'testuser' and password 'testpass', then navigates to the dashboard page and verifies the page title contains 'Dashboard'."
    
    # Prepare the request
    payload = {"prompt": sample_prompt}
    headers = {"Content-Type": "application/json"}
    
    try:
        print("🚀 Making API call...")
        print(f"Prompt: {sample_prompt}\n")
        
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generated Playwright Test Code:")
            print("=" * 60)
            print(result.get("code", "No code returned"))
            print("=" * 60)
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Flask server.")
        print("Make sure the Flask app is running on port 5001")
        print("Run: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    example_api_call()