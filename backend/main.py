from flask import Flask
from flask_cors import CORS
from routes import routes_bp
from auth import auth_bp
from database import engine, Base, SessionLocal
from models import Utilisateur
from werkzeug.security import generate_password_hash

# Création de l'application Flask
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# création des tables
Base.metadata.create_all(bind=engine)

# Créer un admin par défaut si aucun n'existe
def create_admin():
    db = SessionLocal()
    admin_username = "admin"
    admin_password = "11"

    admin_exist = db.query(Utilisateur).filter_by(username=admin_username).first()
    if not admin_exist:
        hashed_password = generate_password_hash(admin_password)
        admin_user = Utilisateur(username=admin_username, password_hash=hashed_password)
        db.add(admin_user)
        db.commit()
        print("Admin créé avec succès")
    
    db.close()

create_admin()

app.register_blueprint(routes_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
