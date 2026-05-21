from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

# Configuration de la connexion Redis via variables d'environnement
redis_host = 'redis-master'
redis_port = 6379
redis_password = os.environ.get("REDIS_PASS")

def get_redis_client():
    return redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True
    )

@app.route('/')
def home():
    try:
        r = get_redis_client()
        btc = r.get('BTC')
        eth = r.get('ETH')
        
        # Petit template HTML basique pour l'affichage public
        html = f"""
        <html>
            <head><title>Crypto Dashboard</title></head>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h1>📈 Crypto Prices Dashboard 📈</h1>
                <div style="margin: 20px; padding: 20px; border: 1px solid #ccc; display: inline-block;">
                    <h2>Bitcoin (BTC) : <span style="color: green;">{btc or 'En attente...'} $</span></h2>
                    <h2>Ethereum (ETH) : <span style="color: blue;">{eth or 'En attente...'} $</span></h2>
                </div>
                <p>Données lues en direct depuis Redis.</p>
            </body>
        </html>
        """
        return html
    except Exception as e:
        return f"Erreur de connexion à la base de données : {e}", 500

if __name__ == '__main__':
    # On écoute sur le port 5000 sur toutes les interfaces réseau
    app.run(host='0.0.0.0', port=5000)