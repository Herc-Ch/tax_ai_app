import os

from flask import Flask, jsonify, request
from flask_cors import CORS

# Optional: Load environment variables from a .env file if running locally (not needed in Docker)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import openai

app = Flask(__name__)
CORS(app)

# Use the OpenAI API key from the environment, for openai>=1.0.0
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# In-memory store for tax data
tax_data = []


@app.route("/api/submit-tax", methods=["GET", "POST", "PUT", "DELETE"])
def submit_tax():
    if request.method == "POST":
        data = request.json
        # Store the whole entry (could use a unique ID in a real app)
        tax_data.append(data)
        response = {"message": "Received tax info.", "received": data}
        return jsonify(response), 201

    elif request.method == "GET":
        return jsonify(tax_data), 200

    elif request.method == "PUT":
        # Basic example: expects an 'index' field to identify the record
        data = request.json
        idx = data.get("index")
        if idx is not None and 0 <= idx < len(tax_data):
            tax_data[idx] = data
            return jsonify({"message": f"Updated tax info at index {idx}."}), 200
        else:
            return jsonify({"error": "Index not found"}), 404

    elif request.method == "DELETE":
        idx = request.args.get("index", type=int)
        if idx is not None and 0 <= idx < len(tax_data):
            deleted = tax_data.pop(idx)
            return (
                jsonify(
                    {"message": f"Deleted tax info at index {idx}.", "deleted": deleted}
                ),
                200,
            )
        else:
            return jsonify({"error": "Index not found"}), 404


@app.route("/api/ai-tax-advice", methods=["POST"])
def ai_tax_advice():
    data = request.json
    # Extract all relevant fields
    filing_status = data.get("filing_status")
    age = data.get("age")
    country = data.get("country")
    employment_type = data.get("employment_type")
    income = data.get("income")
    work_expenses = data.get("work_expenses", 0)
    mortgage_interest = data.get("mortgage_interest", 0)
    charity_donations = data.get("charity_donations", 0)
    education_expenses = data.get("education_expenses", 0)
    retirement_contributions = data.get("retirement_contributions", 0)
    dependents = data.get("dependents", 0)

    # Build the question for the AI
    question = (
        f"I am a {age}-year-old {filing_status.replace('_', ' ')} living in {country}, "
        f"working as a {employment_type.replace('_', ' ')}, with an annual income of {income} euros, "
        f"work-related expenses of {work_expenses} euros, mortgage interest of {mortgage_interest} euros, "
        f"charitable donations of {charity_donations} euros, education expenses of {education_expenses} euros, "
        f"retirement contributions of {retirement_contributions} euros, and {dependents} dependents. "
        "What general tax advice would you give me in this case?"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI tax advisor."},
                {"role": "user", "content": question},
            ],
            max_tokens=300,
        )
        advice = response.choices[0].message.content.strip()
        return jsonify({"advice": advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
