from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from database import engine
from models import Utilisateur

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

# Inscription (pour le moment non utilisée)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    with Session(engine) as db:
        if db.query(Utilisateur).filter_by(username=username).first():
            return jsonify({"message": "Utilisateur déjà existant"}), 400

        new_user = Utilisateur(username=username, password_hash=generate_password_hash(password))
        db.add(new_user)
        db.commit()
        return jsonify({"message": "Utilisateur créé"}), 201

# Connexion
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    with Session(engine) as db:
        user = db.query(Utilisateur).filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"message": "Identifiants invalides"}), 401

        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

# Vérifier le token et récupérer l’utilisateur
def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except:
        return None

# Récupérer les infos du profil
@auth_bp.route("/profil", methods=["GET"])
def get_profil():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Non autorisé"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"message": "Token invalide"}), 401

    with Session(engine) as db:
        user = db.query(Utilisateur).filter_by(id=user_id).first()
        return jsonify({"username": user.username})

# Modifier le mot de passe
@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Non autorisé"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"message": "Token invalide"}), 401

    data = request.json
    new_password = data["new_password"]

    with Session(engine) as db:
        user = db.query(Utilisateur).filter_by(id=user_id).first()
        user.password_hash = generate_password_hash(new_password)
        db.commit()
        return jsonify({"message": "Mot de passe mis à jour"}), 200
