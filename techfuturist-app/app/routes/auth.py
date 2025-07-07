from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from app.models.users import User
from app import db
from flask_login import login_user, logout_user
import jwt
from datetime import datetime, timedelta
from flask import current_app
from app.auth_utils import token_required
from app.models.users import RoleEnum
from app.models.otp import OTP
from app.utils.mail_utils import send_otp_email
import random
import re

PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email et mot de passe requis.", "danger")
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()
        if user:
            if not user.is_verified:
                flash("Veuillez vérifier votre email avant de vous connecter.", "warning")
                return redirect(url_for('auth.verify_email', email=email))

            if user.check_password(password):
                login_user(user)

                token = jwt.encode({
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }, current_app.config['SECRET_KEY'], algorithm='HS256')

                if user.role == RoleEnum.Admin:
                    redirect_url = url_for('admin.dashboard')
                elif user.role == RoleEnum.Participant:
                    redirect_url = url_for('participant.dashboard')
                else:
                    flash("Rôle inconnu", "danger")
                    return render_template('auth/login.html')

                response = redirect(redirect_url)
                response.set_cookie('auth_token', token, httponly=True)
                flash("Connexion réussie.", "success")
                return response
            else:
                flash("Email ou mot de passe incorrect.", "danger")
        else:
            flash("Utilisateur introuvable.", "danger")

    return render_template('auth/login.html')




@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        last_name = request.form.get('name')
        first_name = request.form.get('firstname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('Confirmpassword')

        if not first_name or not last_name or not email or not password or not confirm_password:
            flash("Tous les champs sont obligatoires.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return render_template('auth/register.html')

        if not PASSWORD_REGEX.match(password):
            flash("Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.", "danger")
            return render_template('auth/register.html')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=RoleEnum.Participant  # par défaut participant
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()

            # Génération et enregistrement OTP
            otp_code = str(random.randint(100000, 999999))
            otp = OTP(email=email, code=otp_code)
            db.session.add(otp)
            db.session.commit()

            send_otp_email(email, otp_code)
            flash("Inscription réussie. Un code de vérification a été envoyé par email.", "success")
            return redirect(url_for('auth.verify_email', email=email))
        except IntegrityError:
            db.session.rollback()
            flash("Cette adresse email est déjà utilisée.", "danger")

    return render_template('auth/register.html')



@bp.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    email = request.args.get('email')
    if not email:
        flash("Aucun email fourni.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        otp_code = request.form.get('otp')
        if not otp_code:
            flash("Veuillez saisir le code de vérification.", "danger")
            return render_template('auth/verify_email.html', email=email)

        otp = OTP.query.filter_by(email=email, code=otp_code).first()

        if otp and not otp.is_expired():
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                db.session.commit()
                db.session.delete(otp)
                db.session.commit()
                flash("Email vérifié avec succès. Vous pouvez maintenant vous connecter.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Utilisateur introuvable.", "danger")
        else:
            flash("Code invalide ou expiré.", "danger")

    return render_template('auth/verify_email.html', email=email)


@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth.login'))
