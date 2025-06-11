import os
from datetime import date

import openai
from extensions import db
from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from forms import TaxAdviceForm
from models import TaxRawData

current_year = date.today().year

# create the app
app = Flask(__name__)
# Optional: Load environment variables from a .env file if running locally (not needed in Docker)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tax_data.db"
db.init_app(app)

# Define models here…

with app.app_context():
    db.create_all()


Swagger(app)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")


CORS(
    app, origins=["http://localhost:3000", "https://mytaxapp.com"]
)  # For security reasons in a production scenario

# Use the OpenAI API key from the environment, for openai>=1.0.0
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# In-memory store for tax data
tax_data = []


@app.route("/api/submit-tax", methods=["GET", "POST", "PUT", "DELETE"])
def submit_tax():
    """
    Submit, retrieve, update, or delete tax data records
    ---
    post:
      summary: Submit a new tax record
      consumes:
        - application/json
      parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
              filing_status:
                type: string
                example: single
              age:
                type: integer
                example: 30
              country:
                type: string
                example: Greece
              employment_type:
                type: string
                example: employee
              income:
                type: number
                example: 20000
              work_expenses:
                type: number
                example: 3000
              mortgage_interest:
                type: number
                example: 1000
              charity_donations:
                type: number
                example: 250
              education_expenses:
                type: number
                example: 1200
              retirement_contributions:
                type: number
                example: 900
              dependents:
                type: integer
                example: 2
      responses:
        201:
          description: Tax info received
          schema:
            type: object
            properties:
              message:
                type: string
              received:
                type: object
        400:
          description: Invalid input

    get:
      summary: Retrieve all submitted tax records
      responses:
        200:
          description: A list of tax records
          schema:
            type: array
            items:
              type: object

    put:
      summary: Update a specific tax record by index
      consumes:
        - application/json
      parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
              index:
                type: integer
                description: The index of the record to update
                example: 0
              filing_status:
                type: string
              age:
                type: integer
              country:
                type: string
              employment_type:
                type: string
              income:
                type: number
              work_expenses:
                type: number
              mortgage_interest:
                type: number
              charity_donations:
                type: number
              education_expenses:
                type: number
              retirement_contributions:
                type: number
              dependents:
                type: integer
      responses:
        200:
          description: Record updated
        400:
          description: Invalid input
        404:
          description: Index not found

    delete:
      summary: Delete a specific tax record by index
      parameters:
        - in: query
          name: index
          required: true
          type: integer
          description: The index of the record to delete
          example: 0
      responses:
        200:
          description: Record deleted
        404:
          description: Index not found
    """
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
    """
    Submit tax data and get AI advice
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            filing_status:
              type: string
              description: Filing status of the user (e.g., single, married)
            age:
              type: integer
              description: Age of the user
            country:
              type: string
              description: Country of residence
            employment_type:
              type: string
              description: Employment type (e.g., employee, self-employed)
            income:
              type: number
              description: Annual income
            work_expenses:
              type: number
              description: Work-related expenses
            mortgage_interest:
              type: number
              description: Mortgage interest paid
            charity_donations:
              type: number
              description: Charitable donations made
            education_expenses:
              type: number
              description: Education expenses
            retirement_contributions:
              type: number
              description: Retirement contributions
            dependents:
              type: integer
              description: Number of dependents
    responses:
      200:
        description: Returns AI tax advice
        schema:
          type: object
          properties:
            advice:
              type: string
              description: AI-generated tax advice
    """
    # Build and validate form from request JSON
    form = TaxAdviceForm(data=request.json, meta={"csrf": False})

    if not form.validate():
        return jsonify({"errors": form.errors}), 400
    # form data
    age = form.age.data
    filing_status = form.filing_status.data.replace("_", " ")
    country = form.country.data
    employment_type = form.employment_type.data.replace("_", " ")
    income = form.income.data
    work_expenses = form.work_expenses.data
    mortage_interest = form.mortgage_interest.data
    education_expenses = form.education_expenses.data
    charity_expenses = form.charity_donations.data
    retirement_expenses = form.retirement_contributions.data
    num_of_dependents = form.dependents.data
    # Use validated and type-correct data from the form
    question = f"""
        I am a {age}-year-old {filing_status} living in {country},
        working as a {employment_type}, with an annual income of {income} euros,
        work-related expenses of {work_expenses or 0} euros, mortgage interest of {mortage_interest or 0} euros,
        charitable donations of {charity_expenses or 0} euros, education expenses of {education_expenses or 0} euros,
        retirement contributions of {retirement_expenses or 0} euros, and {num_of_dependents or 0} dependents.
        With all these in mind give me three specific, actionable tax recommendations under the {current_year} {country} tax code,
        including example numerical limits or thresholds (e.g., “mortgage interest deductible up to €3 000”;
        charitable donations up to 10% of taxable income”; “retirement contributions deductible up to €1 500”).
        If you are uncertain, state that these are approximate figures. Use 
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
        record = TaxRawData(
            filing_status=filing_status,
            age=age,
            country=country,
            employment_type=employment_type,
            income=income,
            work_expenses=work_expenses or 0,
            mortgage_interest=mortage_interest or 0,
            charity_donations=charity_expenses or 0,
            education_expenses=education_expenses or 0,
            retirement_contributions=retirement_expenses or 0,
            dependents=num_of_dependents or 0,
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({"advice": advice})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
