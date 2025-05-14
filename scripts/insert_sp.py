# This script automatically generates and inserts support plans for all patients
# Each patient receives a plan from their assigned therapists (psych, physio, ot)
from app import create_app
from app.extensions import db
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.models.user import User
from datetime import datetime

# Create Flask app instance
app = create_app()

# Execute logic inside the application context
with app.app_context():
    # Fetch all patients from the database
    patients = Patient.query.all()
    # Fixed datetime to use for all generated support plans
    plan_date = datetime(2025, 5, 13, 10, 0)

    # Map specialty field names to display labels
    role_map = {
        "psych": "Psychotherapist",
        "physio": "Physiotherapist",
        "ot": "Occupational Therapist"
    }

    # For each patient, create a support plan entry from each assigned therapist
    for patient in patients:
        for specialty, label in role_map.items():
            # Dynamically get the therapist ID based on the specialty
            therapist_id = getattr(patient, f"{specialty}_id")
            therapist = User.query.get(therapist_id)
            if therapist:
                content = f"Support plan from {label} for patient {patient.name}"
                plan = SupportPlan(
                    patient_id=patient.id,
                    therapist_id=therapist_id,
                    content=content,
                    date=plan_date,
                    share_with_guardian=True,
                    share_with_sw=True
                )
                db.session.add(plan)
                print(f"✅ Created plan: {content}")

    # Save all support plans to the database
    db.session.commit()
    print("🎉 All support plans added successfully.")
