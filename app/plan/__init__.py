from flask import Blueprint

plan_bp = Blueprint('plan', __name__, template_folder='templates',url_prefix='/plan')

from app.plan import routes  # 必须在下方导入，避免循环依赖
