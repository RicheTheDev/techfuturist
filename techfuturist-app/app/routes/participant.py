from flask import Blueprint, render_template
from app.auth_utils import token_required,role_required
from app.models.users import RoleEnum
from app.models.users import User
from flask import request

bp = Blueprint('participant', __name__, url_prefix='/participant')

from app.models.users import User

@bp.route('/')
@token_required
@role_required(RoleEnum.Admin)
def list_participants(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = 10  # ou 15 selon ton besoin
    pagination = User.query.filter_by(role=RoleEnum.Participant).order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    participants = pagination.items

    return render_template('users/participants/list.html', participants=participants, pagination=pagination, user=current_user)

@bp.route('/dashboard')
@token_required
@role_required(RoleEnum.Participant)
def dashboard(current_user):
    print(f"Utilisateur connecté : {current_user.email}, rôle : {current_user.role}")
    return render_template('dashboard/participant.html', user=current_user)


@bp.route('/view/<int:id>')
@token_required
@role_required(RoleEnum.Admin)
def view_participant(current_user, id):
    participant = User.query.get_or_404(id)
    return render_template('participant/view.html', participant=participant)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Admin)
def edit_participant(current_user, id):
    # logique de modification ici
    pass

@bp.route('/contact/<int:id>', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Admin)
def contact_participant(current_user, id):
    # logique de contact ici
    pass

@bp.route('/delete/<int:id>', methods=['POST'])
@token_required
@role_required(RoleEnum.Admin)
def delete_participant(current_user, id):
    # logique de suppression ici
    pass
