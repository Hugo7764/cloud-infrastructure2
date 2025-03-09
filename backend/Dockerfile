FROM python:3.9

WORKDIR /backend

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ajout du répertoire backend au PYTHONPATH pour éviter certains problèmes
ENV PYTHONPATH=/backend

# Exposition du port de Flask
EXPOSE 5000

# Démarrage de l'application
CMD python main.py
