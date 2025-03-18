# Utiliser une image Python officielle
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y mariadb-client default-libmysqlclient-dev build-essential


# Copier le fichier requirements.txt
COPY requirements.txt /app/

# Mise à jour de pip et installation des dépendances Python
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet après installation des dépendances
COPY . /app

# Exposer le port 8000 pour Django
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
