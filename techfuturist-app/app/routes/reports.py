from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import current_user
from app import db
from app.auth_utils import token_required, role_required
from app.models.users import RoleEnum
from app.models.report import Report, ReportStatusEnum
from werkzeug.utils import secure_filename
from flask import current_app
import os
from datetime import datetime
from sqlalchemy import extract

bp = Blueprint('reports', __name__, url_prefix='/reports')



# -------------------- LIST REPORTS --------------------


@bp.route('/')
@token_required
def index(current_user):
    if current_user.role in [RoleEnum.Admin, RoleEnum.Mentor]:
        reports = Report.query.all()
    else:
        reports = Report.query.filter_by(submitted_by=current_user.id).all()

    total_submitted = len(reports)
    total_approved = len([r for r in reports if r.status == ReportStatusEnum.Approved])
    total_in_review = len([r for r in reports if r.status == ReportStatusEnum.InReview])

    # Optionnel: calcul des rapports soumis ce mois
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    reports_this_month = Report.query.filter(
        extract('month', Report.submitted_at) == current_month,
        extract('year', Report.submitted_at) == current_year
    ).count()

    return render_template(
        'reports/index.html',
        reports=reports,
        user=current_user,
        total_submitted=total_submitted,
        total_approved=total_approved,
        total_in_review=total_in_review,
        reports_this_month=reports_this_month
    )


@bp.route('/participant')
@token_required
def participant(current_user):
    if current_user.role in [RoleEnum.Admin, RoleEnum.Mentor]:
        reports = Report.query.all()
    else:
        reports = Report.query.filter_by(submitted_by=current_user.id).all()
    return render_template('reports/participant/index.html', reports=reports, user=current_user)

# -------------------- CREATE REPORT --------------------
@bp.route('/create', methods=['GET', 'POST'])
@token_required
def create(current_user):
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        submission_deadline = request.form.get('submission_deadline', '').strip()
        file = request.files.get('file')

        errors = []

        # Validation serveur obligatoire
        if not title:
            errors.append("Le titre est obligatoire.")
        if not file or file.filename.strip() == '':
            errors.append("Le fichier est obligatoire.")

        # Validation de la date de soumission
        deadline_date = None
        if submission_deadline:
            try:
                deadline_date = datetime.strptime(submission_deadline, '%Y-%m-%d')
            except ValueError:
                errors.append("La date de soumission est invalide (format attendu : AAAA-MM-JJ).")

        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for('reports.create'))

        # Enregistrement sécurisé du fichier
        filename = secure_filename(file.filename)
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads', 'reports')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        file_url = f"/static/uploads/reports/{filename}"
        file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'inconnu'

        # Création et sauvegarde du rapport
        report = Report(
            title=title,
            description=description,
            file_url=filename,  # on stocke le nom, pas le chemin complet
            file_type=file_type,
            submission_deadline=deadline_date,
            submitted_by=current_user.id
        )
        db.session.add(report)
        db.session.commit()

        flash("Rapport soumis avec succès.", "success")
        return redirect(url_for('reports.participant'))

    return render_template('reports/participant/add.html', user=current_user)

# -------------------- EDIT REPORT ADMIN/MENTOR --------------------
@bp.route('/admin/edit/<int:report_id>', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Admin)
def edit_admin(current_user, report_id):
    report = Report.query.get_or_404(report_id)

    if request.method == 'POST':
        report.title = request.form.get('title')
        report.description = request.form.get('description')
        submission_deadline = request.form.get('submission_deadline')
        if submission_deadline:
            report.submission_deadline = datetime.strptime(submission_deadline, '%Y-%m-%d')

        # Upload d'un nouveau fichier
        file = request.files.get('file')
        if file and file.filename:
            if report.file_url:
                old_file_path = os.path.join(current_app.root_path, report.file_url[1:])
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            report.file_url = f"/static/uploads/reports/{filename}"
            report.file_type = filename.rsplit('.', 1)[1].lower()

        # Champs spécifiques Admin/Mentor
        report.feedback = request.form.get('feedback')
        status = request.form.get('status')
        if status in [e.name for e in ReportStatusEnum]:
            report.status = ReportStatusEnum[status]

        db.session.commit()
        flash("Rapport mis à jour avec succès.", "success")
        return redirect(url_for('reports.index'))

    return render_template('reports/add.html', report=report, user=current_user, statuses=ReportStatusEnum)

# -------------------- EDIT REPORT PARTICIPANT --------------------

@bp.route('/participant/edit/<int:report_id>', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Participant)
def edit_participant(current_user, report_id):
    report = Report.query.get_or_404(report_id)

    if current_user.id != report.submitted_by:
        flash("Accès refusé.", "danger")
        return redirect(url_for('reports.index'))

    if request.method == 'POST':
        report.title = request.form.get('title')
        report.description = request.form.get('description')
        submission_deadline = request.form.get('submission_deadline')
        if submission_deadline:
            report.submission_deadline = datetime.strptime(submission_deadline, '%Y-%m-%d')

        # Upload d'un nouveau fichier
        file = request.files.get('file')
        if file and file.filename:
            if report.file_url:
                old_file_path = os.path.join(current_app.root_path, report.file_url[1:])
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            report.file_url = f"/static/uploads/reports/{filename}"
            report.file_type = filename.rsplit('.', 1)[1].lower()

        db.session.commit()
        flash("Rapport mis à jour avec succès.", "success")
        return redirect(url_for('reports.participant'))

    return render_template('reports/participant/add.html', report=report, user=current_user, statuses=ReportStatusEnum)

# -------------------- DOWNLOAD REPORT --------------------
@bp.route('/download/<int:report_id>')
@token_required
def download(current_user, report_id):
    report = Report.query.get_or_404(report_id)

    if current_user.id != report.submitted_by and current_user.role not in [RoleEnum.Admin, RoleEnum.Mentor]:
        flash("Accès refusé.", "danger")
        return redirect(url_for('reports.index'))

    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static/uploads/reports')
    filename = os.path.basename(report.file_url)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        flash("Fichier introuvable.", "danger")
        return redirect(url_for('reports.index'))

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# -------------------- DELETE REPORT --------------------
@bp.route('/delete/<int:report_id>', methods=['POST'])
@token_required
@role_required(RoleEnum.Admin)  
def delete(current_user, report_id):
    report = Report.query.get_or_404(report_id)

    if current_user.id != report.submitted_by and current_user.role != RoleEnum.Admin:
        return jsonify({'status': 'error', 'message': "Accès refusé."}), 403

    if report.file_url:
        file_path = os.path.join(current_app.root_path, report.file_url[1:])
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(report)
    db.session.commit()
    flash('ReApport supprimée avec succès', 'success')
    return redirect(url_for('reports.index'))

