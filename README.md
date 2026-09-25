# Ytasty Crousty

API backend du projet **Ytasty Crousty**, développée en Python avec FastAPI et destinée à gérer les restaurants, les utilisateurs, les produits et les commandes.

Le projet est actuellement en cours de développement. L'architecture de l'application et les modèles de données sont mis en place afin de permettre l'implémentation progressive des différentes fonctionnalités de l'API.

---

## Technologies utilisées

* **Python 3.11+**
* **FastAPI** — création de l'API REST
* **Uvicorn** — serveur ASGI
* **SQLAlchemy** — ORM et gestion des modèles de données
* **PostgreSQL 15** — système de gestion de base de données
* **Pydantic** — validation et gestion des données
* **Passlib / bcrypt** — hachage et vérification des mots de passe
* **Docker** — conteneurisation de l'application
* **Docker Compose** — orchestration de l'API et de la base de données
* **uv** — gestion des dépendances et de l'environnement Python

---

## Architecture du projet

```text
Projet-Ytasty-Crousty/
│
├── .env.exemple
├── .gitignore
├── .python-version
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── SchemaSQLPython.pdf
├── uv.lock
│
└── src/
    └── ytasty_crousty/
        ├── __init__.py
        ├── database.py
        ├── main.py
        ├── seed.py
        │
        └── modules/
            ├── auths/
            │   ├── dependencies.py
            │   ├── jwt.py
            │   ├── router.py
            │   └── security.py
            │
            ├── ordres/
            │   ├── __init__.py
            │   ├── models.py
            │   ├── router.py
            │   └── schemas.py
            │
            ├── products/
            │   ├── __init__.py
            │   ├── models.py
            │   ├── router.py
            │   └── schemas.py
            │
            ├── restaurants/
            │   ├── __init__.py
            │   ├── models.py
            │   ├── router.py
            │   └── schemas.py
            │
            └── users/
                ├── __init__.py
                ├── models.py
                ├── router.py
                └── schemas.py
```

---

## Fonctionnalités

### Gestion des restaurants

Le modèle `Restaurant` permet de gérer :

* l'identifiant du restaurant ;
* son nom ;
* sa ville ;
* son adresse ;
* son état d'ouverture ;
* ses horaires d'ouverture ;
* ses coordonnées de contact.

Les restaurants sont également liés aux produits, aux utilisateurs et aux commandes.

---

### Gestion des utilisateurs

Le modèle `User` permet de gérer :

* le prénom ;
* le nom ;
* le nom d'utilisateur ;
* le mot de passe sous forme de hash ;
* le rôle de l'utilisateur ;
* le restaurant auquel l'utilisateur peut être associé.

Trois rôles sont actuellement définis :

```text
admin
staff
direction
```

Les mots de passe sont sécurisés grâce à **Passlib et bcrypt**.

---

### Authentification

Le projet possède une structure dédiée à l'authentification dans :

```text
src/ytasty_crousty/modules/auths/
```

Le hachage et la vérification des mots de passe sont déjà pris en charge.

La structure JWT est également prévue afin de permettre la mise en place de l'authentification par token.

---

### Gestion des produits

Le modèle `Product` permet de représenter les produits proposés par les restaurants.

Un produit possède notamment :

* un nom ;
* une image ;
* une description ;
* une catégorie ;
* un prix ;
* une disponibilité ;
* une liste d'ingrédients ;
* un restaurant associé.

Les produits sont donc directement liés à un restaurant.

---

### Gestion des commandes

Le projet possède également les modèles nécessaires à la gestion des commandes.

Une commande contient notamment :

* un numéro de commande unique ;
* un restaurant ;
* une date de création ;
* un prix total ;
* un statut ;
* les informations du client ;
* les produits commandés ;
* la quantité de chaque produit ;
* le prix unitaire.

Les statuts prévus pour les commandes sont :

```text
pending
validated
preparing
ready
collected
cancelled
```

Deux modes de retrait sont également définis :

```text
onsite
takeaway
```

---

## Base de données

Le projet utilise **PostgreSQL 15**.

La connexion à la base de données est gérée avec SQLAlchemy.

La variable d'environnement utilisée pour la connexion est :

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/ytasty_db
```

Le fichier `.env.exemple` fournit un exemple de configuration.

La base de données est automatiquement accessible au service API lorsqu'elle est lancée avec Docker Compose.

---

## Données initiales

Le fichier :

```text
src/ytasty_crousty/seed.py
```

permet d'initialiser la base de données.

Il crée notamment plusieurs restaurants de démonstration :

* Ytasty Crousty Aix
* Ytasty Crousty Paris
* Ytasty Crousty Lyon

Un compte administrateur initial est également prévu pour le développement.

> Les identifiants présents dans le fichier `seed.py` sont destinés à l'environnement de développement et doivent être modifiés avant toute utilisation en production.

---

## Installation

### Prérequis

Pour utiliser le projet en local, il est recommandé d'avoir :

* Python 3.11 ou supérieur ;
* Docker ;
* Docker Compose ;
* Git.

Pour une installation avec `uv`, celui-ci doit également être installé.

---

## Installation avec Git

Cloner le dépôt :

```bash
git clone https://github.com/issa-le-goat/Projet-Ytasty-Crousty.git
```

Entrer dans le projet :

```bash
cd Projet-Ytasty-Crousty
```

---

## Lancement avec Docker Compose

La méthode recommandée pour lancer l'environnement de développement est Docker Compose.

Construire et démarrer les services :

```bash
docker compose up --build
```

Deux services sont lancés :

```text
db
api
```

### Base de données

Le service PostgreSQL utilise :

```text
Port : 5432
Base : ytasty_db
Utilisateur : postgres
```

### API

L'API est accessible sur :

```text
http://localhost:8000
```

---

## Vérification de l'API

Une route de santé est actuellement disponible :

```http
GET /health
```

Elle retourne :

```json
{
  "status": "ok"
}
```

Cette route permet de vérifier que l'API fonctionne correctement.

---

## Documentation FastAPI

FastAPI génère automatiquement une documentation interactive de l'API.

Une fois l'application lancée, elle est disponible à l'adresse :

```text
http://localhost:8000/docs
```

La documentation alternative ReDoc est disponible à :

```text
http://localhost:8000/redoc
```

---

## Gestion de la base de données

La connexion SQLAlchemy est centralisée dans :

```text
src/ytasty_crousty/database.py
```

Ce fichier contient notamment :

* la configuration de la connexion PostgreSQL ;
* le moteur SQLAlchemy ;
* la session de base de données ;
* la classe `Base` utilisée par les modèles ;
* la dépendance permettant d'obtenir une session de base de données.

Les modèles SQLAlchemy sont organisés par domaine fonctionnel dans le dossier `modules`.

---

## Organisation modulaire

Le projet est organisé autour de plusieurs domaines :

| Module        | Rôle                         |
| ------------- | ---------------------------- |
| `auths`       | Authentification et sécurité |
| `users`       | Gestion des utilisateurs     |
| `restaurants` | Gestion des restaurants      |
| `products`    | Gestion des produits         |
| `ordres`      | Gestion des commandes        |

Cette organisation permet de séparer les responsabilités et de faciliter l'évolution du projet.

---

## État du projet

L'API contient une route de vérification :

```http
GET /health
```

Et aussi un swagger intégré sur la route:

```http
GET /docs
```

---

## Objectif du projet

L'objectif de **Ytasty Crousty** est de construire une API backend permettant de centraliser la gestion d'une chaîne de restaurants.

À terme, l'API doit permettre de gérer les différents restaurants, leurs produits, leurs utilisateurs et leurs commandes, tout en fournissant un système d'authentification et une base de données centralisée.

---

## Licence

Projet réalisé dans le cadre de la formation **Ynov**.

La licence et les conditions de réutilisation du projet sont à définir.
