from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeLocalField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SupportPlanForm(FlaskForm):
    patient_id = SelectField("Select Patient", coerce=int, validators=[DataRequired()], render_kw={"id": "patient-id-select"})
    plan_date = DateTimeLocalField("Plan Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()], render_kw={"id": "plan-date"})
    content = TextAreaField("Support Plan Content", validators=[DataRequired()], render_kw={"rows": 8, "id": "plan-content"})
    share_guardian = BooleanField("Guardian", render_kw={"id": "share-guardian"})
    share_sw = BooleanField("Support Worker", render_kw={"id": "share-sw"})
    submit = SubmitField("Submit Plan")
