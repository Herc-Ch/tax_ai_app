from extensions import db


class TaxRawData(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    filing_status = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(64), nullable=False)
    employment_type = db.Column(db.String(64), nullable=False)
    income = db.Column(db.Float, nullable=False)
    work_expenses = db.Column(db.Float, default=0)
    mortgage_interest = db.Column(db.Float, default=0)
    charity_donations = db.Column(db.Float, default=0)
    education_expenses = db.Column(db.Float, default=0)
    retirement_contributions = db.Column(db.Float, default=0)
    dependents = db.Column(db.Integer, default=0)
