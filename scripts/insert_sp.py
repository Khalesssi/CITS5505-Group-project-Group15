from app import create_app
from app.extensions import db
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.models.user import User
from datetime import datetime

app = create_app()

with app.app_context():
    patients = Patient.query.all()

    # Planned dates: Two different dates
    plan_dates = [
        datetime(2025, 5, 13, 10, 0),
        datetime(2025, 5, 14, 10, 0)
    ]

    # Map therapist type to display label
    role_map = {
        "psych": "Psychotherapist",
        "physio": "Physiotherapist",
        "ot": "Occupational Therapist"
    }

    for patient in patients:
        for date in plan_dates:
            for specialty, label in role_map.items():
                therapist_id = getattr(patient, f"{specialty}_id")
                therapist = User.query.get(therapist_id)
                if therapist:
                    content = f"Support plan from {label} for patient {patient.name} on {date.strftime('%Y-%m-%d')}"
                    plan = SupportPlan(
                        patient_id=patient.id,
                        therapist_id=therapist_id,
                        content=content,
                        date=date,
                        share_with_guardian=True,
                        share_with_sw=True
                    )
                    db.session.add(plan)
                    print(f"Created plan: {content}")

    db.session.commit()
    print("All support plans added successfully for all patients and therapists.")
