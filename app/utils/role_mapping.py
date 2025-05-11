# app/utils/role_mapping.py
role_to_patient_field = {
    "Guardian": "guardian_id",
    "Support Worker": "sw_id"
}

specialty_to_field = {
    "psych": "psych_id",
    "physio": "physio_id",
    "ot": "ot_id"
}

# def specialty_to_field(specialty):
#     return {
#         'psych': 'psych_id',
#         'physio': 'physio_id',
#         'ot': 'ot_id'
#     }.get(specialty)