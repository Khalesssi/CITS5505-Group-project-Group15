# app/forms/questionnaire_forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields import SelectField

class DailyReportForm(FlaskForm):
    patient_id = SelectField("Patient", coerce=int, validators=[DataRequired()], render_kw={"id": "patient-select"})
    date = DateField("Report Date", validators=[DataRequired()], render_kw={"id": "report-date"})

    # 问题1 - 15（确保 ID 唯一）
    question1 = SelectField("Emotion Stable", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], render_kw={"id": "question1"})
    question2 = SelectField("Pain Present", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], render_kw={"id": "question2"})
    question3 = IntegerField("Energy Level (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"id": "question3"})
    question4 = SelectField("Food Intake", choices=[('Normal', 'Normal'), ('Reduced', 'Reduced'), ('Excessive', 'Excessive')], validators=[DataRequired()], render_kw={"id": "question4"})
    question5 = SelectField("Daily Activities", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], render_kw={"id": "question5"})
    question6 = IntegerField("Physical Training (%)", validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={"id": "question6"})
    question7 = IntegerField("Post-exercise Pain (1-10)", validators=[DataRequired(), NumberRange(min=1, max=10)], render_kw={"id": "question7"})
    question8 = IntegerField("Balance (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"id": "question8"})
    question9 = IntegerField("Self-care Willingness (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"id": "question9"})
    question10 = SelectField("Household Tasks", choices=[("Completed", "Completed"), ("Partially Completed", "Partially Completed"), ("Not Completed", "Not Completed")], validators=[DataRequired()], render_kw={"id": "question10"})
    question11 = SelectField("Skill Learning", choices=[("Good", "Good"), ("Average", "Average"), ("Poor", "Poor")], validators=[DataRequired()], render_kw={"id": "question11"})
    question12 = IntegerField("Emotional Fluctuations(1-10)", validators=[DataRequired(),NumberRange(min=1, max=10)], render_kw={"id": "question12"})
    question13 = IntegerField("Social Willingness (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"id": "question13"})
    question14 = IntegerField("Therapist Response (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)], render_kw={"id": "question14"})
    question15 = SelectField("Signs of Anxiety/Depression", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()], render_kw={"id": "question15"})

    submit = SubmitField("Submit Report")
