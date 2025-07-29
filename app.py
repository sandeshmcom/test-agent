from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your API key
openai.api_key = "sk-xxxxxxxxxxxxxxxx"

@app.route('/generate', methods=['POST'])
def generate_test():
    data = request.get_json()
    prompt = data.get("prompt", "")

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in writing Playwright test scripts using @playwright/test."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    code = response.choices[0].message.content
    return jsonify({"code": code})

if __name__ == '__main__':
    app.run(port=5001)