### Description de l'application

# Contexte

L'objectif de cette application est de permettre aux utilisateurs de créer leur propre tounoi 
en ligne, ce tournoi peut être un sport ou n'importe quel jeu en ligne nécessitant un classement et/ou un calendrier de matchs.

L'administrateur de la ligue ajoute les équipes et les matchs, puis édite les scores au fur et à mesure de la compétition.
Les utilisateurs peuvent consulter le calendrier et le classement à tout moment. 

# Utilisation du projet

REQUIS : Docker et Docker Compose installés sur votre machine

1. Télécharger le projet
2. Entrer "docker compose up"
3. Si la base de données est trop lente à démarrer et a créé une erreur fatale dans le backend :
    - Annuler le processus (ctrl + C)
    - Entrer à nouveau "docker compose up"
4. Entrer l'URL "localhost:8080" dans votre navigateur web

### Technologies utilisées

# Frontend
- Vue.js version 3 : framework javascript simple à utiliser et très léger sur l'application
- tailwind.css : framework css là aussi très simple à intégrer au projet
- JWT : Jawa Web token pour l'authentification, solution simple et sécurisée

# Backend
- Flask : framework python pour créer l'API, assez standard et robuste
- SQLAlchemy : ORM permettant de grandement faciliter la réalisation de requêtes en base de donnée par le backend

# Base de donnée
- PostgreSQL : bdd standard correspondant aux besoins du projet

# Conteneurisation
- Docker : permet de créer des conteneurs isolant les différents services de l'application et permettant leur portabilité
- Docker Compose : service d'orchestration des conteneurs dockers permettant leur mise en relation
et le bon fonctionnement de l'application. Permet aussi l'ajout d'un volume qui stocke les données de manière persistante
