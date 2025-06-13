from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional


class TaxAdviceForm(FlaskForm):
    filing_status = StringField("Filing Status", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=18, max=98)])
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
