from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from auth import verify_token
from database import engine
from models import Equipe, Match
from datetime import datetime, timedelta
from functools import wraps
import random

routes_bp = Blueprint("routes", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not verify_token(token):
            return jsonify({"error": "Accès interdit. Authentification requise."}), 403
        return f(*args, **kwargs)
    return decorated_function

# 🏆 Récupérer toutes les équipes
@routes_bp.route("/api/equipes", methods=["GET"])
def get_equipes():
    with Session(engine) as db:
        equipes = db.query(Equipe).all()
        return jsonify([{"id": e.id, "nom": e.nom} for e in equipes])
    
# 🏆 Récupérer une équipe spécifique par son ID
@routes_bp.route("/api/equipes/<int:equipe_id>", methods=["GET"])
def get_equipe(equipe_id):
    with Session(engine) as db:
        equipe = db.query(Equipe).filter_by(id=equipe_id).first()
        if equipe:
            return jsonify({"id": equipe.id, "nom": equipe.nom})
        return jsonify({"message": "Équipe non trouvée"}), 404

# 🏆 Ajouter une nouvelle équipe
@routes_bp.route("/api/equipes", methods=["POST"])
def create_equipe():
    data = request.json
    with Session(engine) as db:
        nouvelle_equipe = Equipe(nom=data["nom"])
        db.add(nouvelle_equipe)
        db.commit()
        return jsonify({"message": "Équipe ajoutée"}), 201
    
# 🏆 Modifier une équipe
@routes_bp.route("/api/equipes/<int:equipe_id>", methods=["PUT"])
def update_equipe(equipe_id):
    data = request.json
    with Session(engine) as db:
        equipe = db.query(Equipe).filter_by(id=equipe_id).first()
        if equipe:
            equipe.nom = data.get("nom", equipe.nom)
            db.commit()
            return jsonify({"message": "Équipe mise à jour"}), 200
        return jsonify({"message": "Équipe introuvable"}), 404

@routes_bp.route("/api/equipes/<int:equipe_id>", methods=["DELETE"])
def delete_equipe(equipe_id):
    with Session(engine) as db:
        # 📌 Vérifier si l'équipe existe
        equipe = db.query(Equipe).filter_by(id=equipe_id).first()
        if not equipe:
            return jsonify({"message": "Équipe introuvable"}), 404

        # 📌 Supprimer d'abord les matchs où l'équipe est impliquée
        db.query(Match).filter(
            (Match.equipe1_id == equipe_id) | (Match.equipe2_id == equipe_id)
        ).delete(synchronize_session=False)

        # 📌 Supprimer l'équipe
        db.delete(equipe)
        db.commit()

        return jsonify({"message": "Équipe et ses matchs supprimés avec succès"}), 200

# 🏟️ Récupérer tous les matchs
@routes_bp.route("/api/matchs", methods=["GET"])
def get_matchs():
    with Session(engine) as db:
        matchs = db.query(Match).all()
        return jsonify([{
            "id": m.id,
            "equipe1_id": m.equipe1_id,
            "equipe2_id": m.equipe2_id,
            "date": m.date.strftime("%Y-%m-%d %H:%M"),
            "score_equipe1": m.score_equipe1,
            "score_equipe2": m.score_equipe2
        } for m in matchs])

# 🏟️ Récupérer un match spécifique par son ID
@routes_bp.route("/api/matchs/<int:match_id>", methods=["GET"])
def get_match(match_id):
    with Session(engine) as db:
        match = db.query(Match).filter_by(id=match_id).first()
        if match:
            return jsonify({
                "id": match.id,
                "equipe1_id": match.equipe1_id,
                "equipe2_id": match.equipe2_id,
                "date": match.date.strftime("%Y-%m-%d %H:%M"),
                "score_equipe1": match.score_equipe1,
                "score_equipe2": match.score_equipe2
            })
        return jsonify({"message": "Match introuvable"}), 404
    
# 🏟️ Ajouter un match
@routes_bp.route("/api/matchs", methods=["POST"])
def create_match():
    data = request.json
    with Session(engine) as db:
        nouveau_match = Match(
            equipe1_id=data["equipe1_id"],
            equipe2_id=data["equipe2_id"],
            date=datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
        )
        db.add(nouveau_match)
        db.commit()
        return jsonify({"message": "Match ajouté"}), 201

# 🏟️ Mettre à jour le score d’un match
@routes_bp.route("/api/matchs/<int:match_id>", methods=["PUT"])
def update_match_score(match_id):
    data = request.json
    with Session(engine) as db:
        match = db.query(Match).filter(Match.id == match_id).first()
        if match:
            match.score_equipe1 = data["score_equipe1"]
            match.score_equipe2 = data["score_equipe2"]
            db.commit()
            return jsonify({"message": "Score mis à jour"}), 200
        return jsonify({"message": "Match introuvable"}), 404
    
# 🏟️ Supprimer un match
@routes_bp.route("/api/matchs/<int:match_id>", methods=["DELETE"])
def delete_match(match_id):
    with Session(engine) as db:
        match = db.query(Match).filter_by(id=match_id).first()
        if match:
            db.delete(match)
            db.commit()
            return jsonify({"message": "Match supprimé"}), 200
        return jsonify({"message": "Match introuvable"}), 404

# 📊 Récupérer le classement amélioré avec statistiques détaillées
@routes_bp.route("/api/classement", methods=["GET"])
def get_classement():
    with Session(engine) as db:
        equipes = db.query(Equipe).all()
        classement = []

        for equipe in equipes:
            matchs_joues = db.query(Match).filter(
                (Match.equipe1_id == equipe.id) | (Match.equipe2_id == equipe.id)
            ).all()

            # Calcul des statistiques
            joues = len(matchs_joues)
            victoires = sum(
                (m.equipe1_id == equipe.id and m.score_equipe1 > m.score_equipe2) or 
                (m.equipe2_id == equipe.id and m.score_equipe2 > m.score_equipe1)
                for m in matchs_joues
            )
            nuls = sum(m.score_equipe1 == m.score_equipe2 for m in matchs_joues)
            defaites = joues - victoires - nuls
            bp = sum(m.score_equipe1 if m.equipe1_id == equipe.id else m.score_equipe2 for m in matchs_joues)
            bc = sum(m.score_equipe2 if m.equipe1_id == equipe.id else m.score_equipe1 for m in matchs_joues)
            diff = bp - bc
            points = victoires * 3 + nuls  # 3 points pour une victoire, 1 pour un nul

            classement.append({
                "nom": equipe.nom,
                "joues": joues,
                "victoires": victoires,
                "nuls": nuls,
                "defaites": defaites,
                "bp": bp,
                "bc": bc,
                "diff": diff,
                "points": points
            })

        # Tri du classement par points, puis différence de buts
        classement.sort(key=lambda x: (x["points"], x["diff"], x["bp"]), reverse=True)

        return jsonify(classement)
    
@routes_bp.route("/api/generate-test-data", methods=["POST"])
def generate_test_data():
    with Session(engine) as db:
        # 📌 1. Ajouter les équipes
        equipes_noms = [
            "Paris Saint-Germain", "AS Monaco", "LOSC Lille", "OGC Nice", "Olympique Lyonnais",
            "Stade Brestois 29", "RC Lens", "Olympique de Marseille", "Stade Rennais FC", 
            "Montpellier HSC", "Toulouse FC", "FC Nantes", "RC Strasbourg Alsace",
            "Stade de Reims", "Le Havre AC", "AJ Auxerre", "Angers SCO", "AS Saint-Étienne"
        ]

        equipes = []
        for nom in equipes_noms:
            equipe = db.query(Equipe).filter_by(nom=nom).first()
            if not equipe:
                equipe = Equipe(nom=nom)
                db.add(equipe)
            equipes.append(equipe)

        db.commit()

        # 📌 2. Générer un championnat complet (chaque équipe affronte toutes les autres)
        date_debut = datetime.now() + timedelta(days=1)
        matchs = []
        for i in range(len(equipes)):
            for j in range(i + 1, len(equipes)):
                equipe1, equipe2 = equipes[i], equipes[j]
                score1, score2 = random.randint(0, 5), random.randint(0, 5)  # Scores aléatoires
                match = Match(
                    equipe1_id=equipe1.id,
                    equipe2_id=equipe2.id,
                    date=date_debut,
                    score_equipe1=score1,
                    score_equipe2=score2
                )
                matchs.append(match)
                date_debut += timedelta(days=1)  # Un match par jour

        db.add_all(matchs)
        db.commit()

        return jsonify({"message": "Données de test générées avec succès !"}), 201

# 🔄 Générer un calendrier complet équilibré
@routes_bp.route("/api/generer-calendrier", methods=["POST"])
def generer_calendrier():
    with Session(engine) as db:
        # 📌 Supprimer tous les anciens matchs
        db.query(Match).delete()

        # 📌 Récupérer toutes les équipes existantes
        equipes = db.query(Equipe).all()
        if len(equipes) < 2:
            return jsonify({"message": "Il faut au moins 2 équipes pour générer un calendrier"}), 400

        # 📌 Générer une liste de toutes les rencontres possibles (chaque équipe affronte toutes les autres)
        matchs_possibles = [(e1.id, e2.id) for i, e1 in enumerate(equipes) for e2 in equipes[i+1:]]

        # 📌 Mélanger les matchs pour équilibrer les rencontres
        random.shuffle(matchs_possibles)

        # 📌 Définir la date de début (exemple : lundi prochain)
        date_match = datetime.now() + timedelta(days=(7 - datetime.now().weekday()))

        # 📌 Générer un calendrier où chaque équipe joue 1 match par semaine
        matchs = []
        while matchs_possibles:
            semaine_matchs = []
            equipes_jouees = set()

            for equipe1_id, equipe2_id in matchs_possibles[:]:  # Copie de la liste pour modification
                if equipe1_id not in equipes_jouees and equipe2_id not in equipes_jouees:
                    matchs.append(Match(
                        equipe1_id=equipe1_id,
                        equipe2_id=equipe2_id,
                        date=date_match
                    ))
                    equipes_jouees.update([equipe1_id, equipe2_id])
                    matchs_possibles.remove((equipe1_id, equipe2_id))

            date_match += timedelta(weeks=1)  # 🔄 Passer à la semaine suivante

        # 📌 Enregistrer les matchs en base de données
        db.add_all(matchs)
        db.commit()

        return jsonify({"message": "Calendrier généré avec succès !"}), 201
    