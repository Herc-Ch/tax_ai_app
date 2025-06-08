import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional

# Optional: Load environment variables from a .env file if running locally (not needed in Docker)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import openai


class TaxAdviceForm(FlaskForm):
    filing_status = StringField("Filing Status", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=18, max=99)])
    country = StringField("Country", validators=[DataRequired()])
    employment_type = StringField("Employment Type", validators=[DataRequired()])
    income = FloatField("Income", validators=[DataRequired(), NumberRange(min=0)])
    work_expenses = FloatField("Work Expenses", validators=[Optional()])
    mortgage_interest = FloatField("Mortgage Interest", validators=[Optional()])
    charity_donations = FloatField("Charity Donations", validators=[Optional()])
    education_expenses = FloatField("Education Expenses", validators=[Optional()])
    retirement_contributions = FloatField(
        "Retirement Contributions", validators=[Optional()]
    )
    dependents = IntegerField("Dependents", validators=[Optional(), NumberRange(min=0)])


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
CORS(app)

# Use the OpenAI API key from the environment, for openai>=1.0.0
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# In-memory store for tax data
tax_data = []


@app.route("/api/submit-tax", methods=["GET", "POST", "PUT", "DELETE"])
def submit_tax():
    if request.method == "POST":
        # Validate the incoming data using TaxAdviceForm
        form = TaxAdviceForm(data=request.json, meta={"csrf": False})
        if not form.validate():
            return jsonify({"errors": form.errors}), 400
        # Use form.data (or a copy to avoid WTForms internal state)
        record = {key: value for key, value in form.data.items() if key != "csrf_token"}
        tax_data.append(record)
        response = {"message": "Received tax info.", "received": record}
        return jsonify(response), 201

    elif request.method == "GET":
        return jsonify(tax_data), 200

    elif request.method == "PUT":
        data = request.json
        idx = data.get("index")
        # Validate the update data (excluding the index itself)
        form = TaxAdviceForm(data=data, meta={"csrf": False})
        if not form.validate():
            return jsonify({"errors": form.errors}), 400
        if idx is not None and 0 <= idx < len(tax_data):
            # Use only validated form data, not the raw input
            updated_record = {
                key: value for key, value in form.data.items() if key != "csrf_token"
            }
            tax_data[idx] = updated_record
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
    # Build and validate form from request JSON
    form = TaxAdviceForm(data=request.json, meta={"csrf": False})

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    # Use validated and type-correct data from the form
    question = f"""
        I am a {form.age.data}-year-old {form.filing_status.data.replace('_', ' ')} living in {form.country.data},
        working as a {form.employment_type.data.replace('_', ' ')}, with an annual income of {form.income.data} euros,
        work-related expenses of {form.work_expenses.data or 0} euros, mortgage interest of {form.mortgage_interest.data or 0} euros,
        charitable donations of {form.charity_donations.data or 0} euros, education expenses of {form.education_expenses.data or 0} euros,
        retirement contributions of {form.retirement_contributions.data or 0} euros, and {form.dependents.data or 0} dependents.
        Please give me three specific, actionable tax recommendations under the 2025 Greek tax code,
        including example numerical limits or thresholds (e.g., “mortgage interest deductible up to €3 000”;
        charitable donations up to 10% of taxable income”; “retirement contributions deductible up to €1 500”).
        If you are uncertain, state that these are approximate figures.
    """

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
