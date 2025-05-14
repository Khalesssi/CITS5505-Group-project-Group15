from flask import render_template
from collections import defaultdict
from app.dashboard import dashboard_bp 
from flask_login import login_required
from flask_login import current_user
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.models.user import User
from app.utils.role_mapping import role_to_patient_field    
from app.utils.role_mapping import specialty_to_field
from app.models.user import User
from flask import flash, redirect, url_for
# from app import db
from datetime import datetime
from flask import request
from app.extensions import db
from flask import render_template
from app.forms.plan_forms import SupportPlanForm
from app.forms.questionnaire_forms import DailyReportForm



@dashboard_bp.route('/guardian')
@login_required
def guardian_dashboard():
    # 获取绑定病人
    patients = Patient.query.filter_by(guardian_id=current_user.id).all()
    patient_ids = [p.id for p in patients]

    # 获取已分享的支持计划
    all_plans = SupportPlan.query.filter(
        SupportPlan.patient_id.in_(patient_ids),
        SupportPlan.share_with_guardian == True
    ).all()

    # 提取有效病人和日期
    plan_patient_ids = list({plan.patient_id for plan in all_plans})
    plan_dates = sorted(list({plan.date.date() for plan in all_plans}))

    # 获取筛选参数
    selected_patient_id = request.args.get('patient_id', type=int)
    selected_date_str = request.args.get('plan_date')
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else None

    # 仅当同时选中了病人和日期才显示计划
    if selected_patient_id and selected_date:
        filtered_plans = [
            plan for plan in all_plans
            if plan.patient_id == selected_patient_id and plan.date.date() == selected_date
        ]
    else:
        filtered_plans = []

    # 分组
    grouped_plans = defaultdict(list)
    for plan in filtered_plans:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped_plans[therapist.specialty].append(plan)

    return render_template(
        'dashboard/guardian.html',
        patients=patients,
        grouped_plans=grouped_plans,
        plan_patient_ids=plan_patient_ids,
        plan_dates=plan_dates,
        selected_patient_id=selected_patient_id,
        selected_date_str=selected_date_str
    )

@dashboard_bp.route('/sw')
@login_required
def sw_dashboard():
    # 获取绑定病人
    patients = Patient.query.filter_by(sw_id=current_user.id).all()
    patient_ids = [p.id for p in patients]

    form = DailyReportForm()
    form.patient_id.choices = [(p.id, p.name) for p in patients]

    # 获取已分享的支持计划
    all_plans = SupportPlan.query.filter(
        SupportPlan.patient_id.in_(patient_ids),
        SupportPlan.share_with_sw == True
    ).all()

    # 提取有效病人和日期
    plan_patient_ids = list({plan.patient_id for plan in all_plans})
    plan_dates = sorted(list({plan.date.date() for plan in all_plans}))

    # 获取筛选参数
    selected_patient_id = request.args.get('patient_id', type=int)
    selected_date_str = request.args.get('plan_date')
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else None

    # 如果都选中才显示
    if selected_patient_id and selected_date:
        filtered_plans = [
            plan for plan in all_plans
            if plan.patient_id == selected_patient_id and plan.date.date() == selected_date
        ]
    else:
        filtered_plans = []

    # 分组
    grouped_plans = defaultdict(list)
    for plan in filtered_plans:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped_plans[therapist.specialty].append(plan)

    return render_template(
        'dashboard/sw.html',  # ✅ 与 guardian 共用模板
        form=form,
        patients=patients,
        grouped_plans=grouped_plans,
        plan_patient_ids=plan_patient_ids,
        plan_dates=plan_dates,
        selected_patient_id=selected_patient_id,
        selected_date_str=selected_date_str
    )


@dashboard_bp.route('/therapist')
@login_required
def therapist_dashboard():
    field = specialty_to_field.get(current_user.specialty)
    patients = Patient.query.filter(getattr(Patient, field) == current_user.id).all() if field else []
    form = SupportPlanForm()
    form.patient_id.choices = [(p.id, p.name) for p in patients]
    return render_template('dashboard/therapist.html', patients=patients, form=form)


@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != "Admin":
        flash("Access denied.")
        return redirect(url_for("auth.login"))
    
    users = User.query.all()
    return render_template('dashboard/admin.html', users=users)

# 这个部分应该是为了处理导航栏dashboard 的跳转
@dashboard_bp.route('/redirect')
@login_required
def dashboard_redirect():
    role = current_user.role
    if role == "Support Worker":
        return redirect(url_for("dashboard.sw_dashboard"))
    elif role == "Guardian":
        return redirect(url_for("dashboard.guardian_dashboard"))
    elif role == "Therapist":
        return redirect(url_for("dashboard.therapist_dashboard"))
    elif role == "Admin":
        return redirect(url_for("dashboard.admin_dashboard"))
    else:
        flash("No dashboard defined for this role.")
        return redirect(url_for("auth.login"))





