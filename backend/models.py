from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Ajout des modèles de la bdd dans SQLAlchemy

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

class Equipe(Base):
    __tablename__ = "equipes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)

    matchs_domicile = relationship("Match", foreign_keys="[Match.equipe1_id]", back_populates="equipe1")
    matchs_exterieur = relationship("Match", foreign_keys="[Match.equipe2_id]", back_populates="equipe2")

class Match(Base):
    __tablename__ = "matchs"

    id = Column(Integer, primary_key=True, index=True)
    equipe1_id = Column(Integer, ForeignKey("equipes.id"))
    equipe2_id = Column(Integer, ForeignKey("equipes.id"))
    date = Column(DateTime, nullable=False)
    score_equipe1 = Column(Integer, default=0)
    score_equipe2 = Column(Integer, default=0)

    equipe1 = relationship("Equipe", foreign_keys=[equipe1_id], back_populates="matchs_domicile")
    equipe2 = relationship("Equipe", foreign_keys=[equipe2_id], back_populates="matchs_exterieur")
