from flask import Blueprint, render_template
from app.auth_utils import token_required,role_required
from app.models.users import RoleEnum

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@token_required
@role_required(RoleEnum.Admin)
def dashboard(current_user):
    print(f"Utilisateur connecté : {current_user.email}, rôle : {current_user.role}")
    return render_template('dashboard/admin.html', user=current_user)
