import requests
import redis
import time

# Configuration de la connexion à notre future base Redis
# On utilise "redis-master" comme nom d'hôte, tu comprendras pourquoi avec Docker !
redis_host = 'redis-master'
redis_port = 6379

def get_redis_connection():
    try:
        return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    except Exception as e:
        print(f"Erreur de connexion à Redis : {e}")
        return None

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    
    try:
        response = requests.get(url)
        
        # 1. On vérifie d'abord si on est bloqué par l'API
        if response.status_code == 429:
            print("Erreur 429 : Trop de requêtes ! L'API nous met en pause.")
            return None
        
        # 2. On vérifie s'il y a une autre erreur (serveur en panne, etc.)
        if response.status_code != 200:
            print(f"Erreur réseau inattendue : Code {response.status_code}")
            return None
            
        data = response.json()
        
        # 3. On vérifie que les clés existent bien avant de les lire
        if 'bitcoin' in data and 'ethereum' in data:
            btc_price = data['bitcoin']['usd']
            eth_price = data['ethereum']['usd']
            
            print(f"Prix récupérés -> BTC: {btc_price}$ | ETH: {eth_price}$")
            return {'BTC': btc_price, 'ETH': eth_price}
        else:
            print(f"Structure JSON inattendue : {data}")
            return None
            
    except Exception as e:
        print(f"Erreur critique du script : {e}")
        return None

if __name__ == "__main__":
    print("Démarrage du Crypto-Fetcher...")
    r = get_redis_connection()
    
    while True:
        prices = fetch_crypto_prices()
        
        if prices and r:
            try:
                # On pousse les prix dans la base de données
                r.set('BTC', prices['BTC'])
                r.set('ETH', prices['ETH'])
                print("Prix mis à jour dans Redis avec succès.")
            except Exception as e:
                print(f"Impossible d'écrire dans Redis (Est-il lancé ?) : {e}")
        
        # On attend 10 secondes avant la prochaine requête
        time.sleep(10)
