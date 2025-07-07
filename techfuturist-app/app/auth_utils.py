from functools import wraps
from flask import request, jsonify, current_app,redirect, url_for, flash
import jwt
from app.models.users import User
from app.models.users import User, RoleEnum # ou from app.models import User selon l'architecture

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            flash("Connexion requise. Veuillez vous connecter.", "warning")
            return redirect(url_for('auth.login'))  # Remplace 'auth.login' si besoin

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                flash("Utilisateur introuvable. Veuillez vous reconnecter.", "danger")
                return redirect(url_for('auth.login'))

        except jwt.ExpiredSignatureError:
            flash("Votre session a expiré. Veuillez vous reconnecter.", "warning")
            return redirect(url_for('auth.login'))
        except jwt.InvalidTokenError:
            flash("Token invalide. Veuillez vous reconnecter.", "danger")
            return redirect(url_for('auth.login'))

        return f(current_user, *args, **kwargs)
    return decorated


def role_required(expected_role: RoleEnum):
    def decorator(f):
        @wraps(f)
        def wrapped(current_user, *args, **kwargs):
            if current_user.role != expected_role:
                return jsonify({'message': 'Accès interdit : rôle insuffisant'}), 403
            return f(current_user, *args, **kwargs)
        return wrapped
    return decorator