from dotenv import load_dotenv
load_dotenv()
import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Make sure to set your OpenAI API key as an environment variable!
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/ai-tax-advice', methods=['POST'])
def ai_tax_advice():
    data = request.json
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    # Call OpenAI API (using GPT-3.5/4, or whichever is provided)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or whatever model your key allows
            messages=[
                {"role": "system", "content": "You are a helpful AI tax advisor."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=300
        )
        advice = completion.choices[0].message.content.strip()
        return jsonify({"advice": advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
