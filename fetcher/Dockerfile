FROM python:3.12-slim

WORKDIR /app

# Forcer Python à afficher les logs en temps réel
ENV PYTHONUNBUFFERED=1

# ça va plus vite --> On copie d'abord le fichier des dépendances --> ça permet de profiter du cache de Docker pour ne pas réinstaller les dépendances à chaque changement de code
COPY requirements.txt .

# On installe les dépendances --> ça peut être long, donc on veut que ça soit mis en cache par Docker
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste du code
COPY . .

# La commande de lancement
CMD ["python", "fetcher.py"]