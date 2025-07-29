import requests
import json
import sys

def call_flask_api(prompt, url="http://localhost:5001/generate"):
    """
    Call the Flask API with a JSON prompt and display the result.
    
    Args:
        prompt (str): The prompt to send to the API
        url (str): The API endpoint URL
    """
    try:
        # Prepare the JSON payload
        payload = {"prompt": prompt}
        
        # Set headers for JSON content
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"🚀 Calling API at: {url}")
        print(f"📝 Prompt: {prompt}\n")
        
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print("=" * 50)
            print(result.get("code", "No code returned"))
            print("=" * 50)
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the Flask server.")
        print("Make sure the Flask app is running on port 5001")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function to handle command line usage or interactive mode."""
    
    # Check if prompt is provided as command line argument
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        call_flask_api(prompt)
    else:
        # Interactive mode
        print("🤖 Flask API Client")
        print("Enter your prompt (or 'quit' to exit):")
        
        while True:
            try:
                prompt = input("\n> ").strip()
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not prompt:
                    print("Please enter a prompt.")
                    continue
                
                call_flask_api(prompt)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    main()