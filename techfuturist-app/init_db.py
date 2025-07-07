from app import create_app, db, bcrypt
from app.models.users import User  # Chemin ajusté selon ton organisation
from app.models.resource import Resource
from app.models.report import Report
from app.models.project import Project
from app.models.question import Question
from app.models.test import Test
from app.models.user_test_result import UserTestResult

app = create_app()

with app.app_context():
    # Création des tables
    db.create_all()
    print("✅ Base de données initialisée avec succès.")

    # Vérification si un admin existe déjà
    existing_admin = User.query.filter_by(email="uassogba06@gmail.com").first()

    if not existing_admin:
        hashed_password = bcrypt.generate_password_hash("Ulrich@2024").decode('utf-8')
        admin = User(
            first_name="Ulrich",
            last_name="ASSOGBA",
            email="uassogba06@gmail.com",
            password_hash=hashed_password,
            role="Admin",  # correspond à l'enum dans User model
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("👑 Utilisateur admin créé avec succès.")
    else:
        print("⚠️ Utilisateur admin déjà existant.")
