from flask import Blueprint, render_template, request, redirect, url_for, flash,send_from_directory
from flask_login import login_required, current_user
from app import db
from app.auth_utils import token_required,role_required
from app.models.users import RoleEnum
from app.models.resource import Resource
from werkzeug.utils import secure_filename
import os
from flask import current_app
from flask import jsonify


bp = Blueprint('resources', __name__, url_prefix='/resources')

# @bp.route('/')
# @token_required
# def index(current_user):
#     resources = Resource.query.all()
#     return render_template('resources/index.html' , resources=resources , user=current_user)

@bp.route('/')
@token_required
def index(current_user):
    resources = Resource.query.all()
    total_resources = Resource.query.count()
    published_resources = Resource.query.filter_by(is_published=True).count()
    total_downloads = db.session.query(db.func.sum(Resource.download_count)).scalar() or 0

    return render_template(
        'resources/index.html',
        resources=resources,
        user=current_user,
        total_resources=total_resources,
        published_resources=published_resources,
        total_downloads=total_downloads
    )


@bp.route('/participant')
@token_required
def participant(current_user):
    resources = Resource.query.all()
    return render_template('resources/participant/index.html' , resources=resources, user=current_user)


@bp.route('/create', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Admin)
def create(current_user):
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        file_type = request.form.get('file_type', '').strip()
        file = request.files.get('file')

        errors = []

        # Validation serveur obligatoire
        if not title:
            errors.append("Le titre est obligatoire.")
        if not file_type:
            errors.append("Le type de ressource est obligatoire.")
        if not file or file.filename.strip() == '':
            errors.append("Le fichier de la ressource est obligatoire.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for('resources.create'))

        # Sécurisation du nom de fichier
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        upload_path = os.path.join(upload_folder, filename)
        file.save(upload_path)

        # Sauvegarde en base
        resource = Resource(
            title=title,
            description=description,
            file_url=filename,  # stocke le nom seul pour le chemin statique
            file_type=file_type,
            uploaded_by=current_user.id
        )
        db.session.add(resource)
        db.session.commit()

        flash("Ressource ajoutée avec succès.", "success")
        return redirect(url_for('resources.index'))

    return render_template('resources/add.html', user=current_user)



@bp.route('/edit/<int:resource_id>', methods=['GET', 'POST'])
@token_required
@role_required(RoleEnum.Admin)
def edit(current_user, resource_id):
    resource = Resource.query.get_or_404(resource_id)

    if request.method == 'POST':
        resource.title = request.form.get('title')
        resource.description = request.form.get('description')
        resource.file_type = request.form.get('file_type')

        file = request.files.get('file')
        if file and file.filename:
            # Supprimer l'ancien fichier si présent
            if resource.file_url:
                # old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url)
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resource.file_url)
                if os.path.exists(old_file_path):
                    print(f"Tentative de suppression: {old_file_path}")
                    print(f"Existe? {os.path.exists(old_file_path)}")
                    os.remove(old_file_path)

            # Enregistrer le nouveau fichier
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            resource.file_url = filename

        db.session.commit()
        flash("Ressource mise à jour avec succès", "success")
        return redirect(url_for('resources.index'))

    return render_template('resources/add.html', resource=resource, user=current_user)




@bp.route('/download/<int:resource_id>')
@token_required
def download(current_user, resource_id):
    resource = Resource.query.get_or_404(resource_id)

    if not resource.file_url:
        flash("Aucun fichier associé à cette ressource.", "danger")
        return redirect(url_for('resources.index'))

    # Extraire le nom de fichier à partir de l'URL enregistrée
    filename = os.path.basename(resource.file_url)

    # Chemin absolu du dossier contenant les fichiers uploadés
    upload_folder = os.path.join(current_app.root_path, 'static/uploads')

    # Vérifier si le fichier existe avant d'envoyer
    file_path = os.path.join(upload_folder, filename)
    if not os.path.exists(file_path):
        flash("Fichier non trouvé sur le serveur.", "danger")
        return redirect(url_for('resources.index'))

    # Envoie le fichier en pièce jointe pour téléchargement
    return send_from_directory(upload_folder, filename, as_attachment=True)




@bp.route('/delete/<int:resource_id>', methods=['POST'])
@token_required
@role_required(RoleEnum.Admin)
def delete(current_user, resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Ressource supprimée avec succès.'})


# @bp.route('/delete/<int:resource_id>', methods=['POST'])
# @token_required
# @role_required(RoleEnum.Admin)
# def delete( current_user,resource_id):
#     resource = Resource.query.get_or_404(resource_id)
#     db.session.delete(resource)
#     db.session.commit()
#     flash("Ressource supprimée", "success")
#     return redirect(url_for('resources.index'))



