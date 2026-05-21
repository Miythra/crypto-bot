 # Crypto-Bot — Lab Kubernetes Sécurité

Laboratoire DevSecOps pour la conception, le déploiement et le durcissement d'une architecture microservices cloud-native (Docker → Kubernetes). Ce dépôt illustre l'isolation réseau via Calico, l'utilisation de NetworkPolicies et des scénarios Red Team / Blue Team.

## Sommaire
- Description
- Architecture
- Prérequis
- Démarrage rapide
- Commandes utiles
- Sécurité & durcissement
- Contribuer

## Description
Le projet contient trois composants principaux :
- `fetcher` : collecte les prix (BTC/ETH) et écrit dans Redis.
- `redis` : base en mémoire, accessible uniquement depuis le cluster.
- `api` : service Flask affichant les données via un tableau de bord web.

L'objectif pédagogique est de montrer comment sécuriser les communications inter-pods avec des NetworkPolicies et un CNI sécurisé (Calico).

## Architecture (vue simplifiée)

[ Navigateur Hôte ] ──(5000)──> [ Pod: crypto-api ]
                                                 │
                                          (6379)
                                                 ▼
                              [ Pod: crypto-fetcher ]
                                                 │
                                                 ▼
                                           [ Pod: redis ]

Un pod non autorisé doit être empêché d'atteindre Redis grâce aux NetworkPolicies.

## Prérequis
- Linux (Ubuntu / Debian recommandé)
- Docker
- kind
- kubectl

## Démarrage rapide
Suivez ces commandes pour créer le cluster local et déployer l'application :

```bash
# 1. Créer un cluster Kind avec configuration Calico
kind create cluster --config kind-config-calico.yaml

# 2. Installer Calico
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.27.3/manifests/calico.yaml

# 3. Créer le secret Redis (exemple)
kubectl create secret generic redis-password --from-literal=password='SuperSecret123!'

# 4. Construire les images
docker build -t crypto-fetcher:v1 ./fetcher
docker build -t crypto-api:v1 ./api

# 5. Charger les images dans Kind
kind load docker-image crypto-fetcher:v1 --name crypto-cluster
kind load docker-image crypto-api:v1 --name crypto-cluster

# 6. Déployer les manifests Kubernetes
kubectl apply -f k8s/
```

Remplacez les secrets et les tags d'image en production par des valeurs adaptées.

## Commandes utiles
- Voir les pods :

```bash
kubectl get pods -A
```

- Logs d'un pod :

```bash
kubectl logs -f deployment/crypto-api
```

- Port-forward pour accéder à l'API localement :

```bash
kubectl port-forward service/crypto-api-service 5000:5000
```

## Sécurité et durcissement
- Utilisation de Calico comme CNI pour des contrôles réseau granulaires.
- NetworkPolicy `default-deny` : bloquer tout trafic entrant par défaut.
- NetworkPolicy spécifique autorisant uniquement `crypto-api` et `crypto-fetcher` à contacter `redis:6379`.
- Stocker les secrets via `kubectl create secret` ou un gestionnaire de secrets chiffré.

Les manifests Kubernetes fournis dans `k8s/` incluent des exemples de NetworkPolicies et de Deployments.

## Contribuer
- Ouvrir une issue pour proposer une amélioration.
- Faire une branche, committer et proposer une Pull Request.

## Licence
Ce dépôt est fourni à des fins d'apprentissage. Adaptez les secrets et configurations avant tout usage en production.

---

Si vous voulez que je reformule certains passages (par ex. le guide pas-à-pas, le PDF de rapport, ou traduire en anglais), dites-moi ce que vous préférez.
