# Banking_sim

API de simulation bancaire construite avec FastAPI, SQLAlchemy et SQLite.

Le projet permet de gerer un mini systeme bancaire :

- creation de clients ;
- creation de comptes rattaches aux clients ;
- virements entre comptes ;
- mise a jour automatique des soldes ;
- enregistrement des transactions ;
- detection simple des transactions a risque.

## Statut du projet

Le projet est fonctionnel pour une utilisation locale, une demonstration ou un prototype backend.

Il n'est pas encore pret pour une mise en production reelle sans ajouter au minimum :

- des tests automatises ;
- une authentification ;
- une configuration CORS stricte ;
- des migrations de base de donnees ;
- une base de donnees de production ;
- une strategie de logs et de monitoring ;
- une gestion des secrets par variables d'environnement.

## Architecture

```text
Banking_sim/
├── app/
│   ├── main.py                 # Point d'entree FastAPI
│   ├── database.py             # Configuration SQLAlchemy / SQLite
│   ├── models.py               # Modeles SQLAlchemy
│   ├── schemas.py              # Schemas Pydantic
│   ├── crud.py                 # Logique metier principale
│   ├── seed.py                 # Script de remplissage de la base
│   └── routes/
│       ├── clients.py          # Routes clients
│       ├── accounts.py         # Routes comptes
│       └── transactions.py     # Routes transactions
├── service/
│   └── risk_engine.py          # Moteur de risque simple
├── data/
│   └── bank.db                 # Base SQLite locale
├── requirements.txt            # Dependances Python
├── makefile                    # Automatisation future
└── README.md
```


## Prerequis

- Python 3.9 ou plus recent
- `pip`
- un terminal
- optionnel : un client HTTP comme Swagger, curl, Postman ou Insomnia

## Installation locale

Depuis la racine du projet :

```bash
make install
```

Cette commande cree le dossier `venv/` et installe les dependances depuis `requirements.txt`.

Equivalent manuel :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Commandes Makefile

Le projet contient un `makefile` simple pour eviter de retaper les commandes longues.

| Commande | Description |
| --- | --- |
| `make help` | Affiche les commandes disponibles |
| `make install` | Cree le venv et installe les dependances |
| `make seed` | Remplit la base SQLite avec des donnees de test |
| `make run` | Lance l'API en mode developpement |
| `make serve` | Lance l'API en mode serveur local |
| `make check` | Verifie la syntaxe et l'import de l'application |
| `make routes` | Affiche les routes FastAPI disponibles |
| `make clean` | Supprime les caches Python |

Workflow recommande :

```bash
make install
make seed
make run
```

## Configuration

Par defaut, l'application utilise SQLite :

```text
sqlite:///./data/bank.db
```

La configuration est definie dans `app/database.py`.

Il est possible de changer la base utilisee avec la variable d'environnement `DATABASE_URL` :

```bash
export DATABASE_URL="sqlite:///./data/bank.db"
```

Exemple pour une future base PostgreSQL :

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/banking"
```

Attention : la configuration actuelle de `create_engine` contient `check_same_thread=False`, utile pour SQLite. Pour PostgreSQL, il faudra adapter la configuration SQLAlchemy.

## Initialiser la base

Pour remplir la base avec des donnees de test :

```bash
make seed
```

Le script :

1. supprime les transactions existantes ;
2. supprime les comptes existants ;
3. supprime les clients existants ;
4. cree une liste de clients ;
5. cree un compte par client avec un solde aleatoire.

## Lancer l'API en developpement

```bash
make run
```

URLs utiles (Lors du lancement, aller sur http://127.0.0.1:8000/docs !!):

```text
API locale:       http://127.0.0.1:8000
Swagger UI:       http://127.0.0.1:8000/docs
OpenAPI schema:   http://127.0.0.1:8000/openapi.json
```

## Lancer l'API en mode serveur

Pour un lancement sans rechargement automatique :

```bash
make serve
```

Pour un vrai deploiement, utiliser plutot un processus supervise :

- Docker ;
- systemd ;
- Gunicorn avec workers Uvicorn ;
- une plateforme cloud ;
- un reverse proxy comme Nginx ou Traefik.

Exemple Gunicorn :

```bash
pip install gunicorn

PYTHONPATH=. gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Fonctionnement general

Au demarrage, `app/main.py` :

1. cree l'application FastAPI ;
2. configure CORS ;
3. cree les tables SQLAlchemy si elles n'existent pas ;
4. branche les routes clients, comptes et transactions.

La logique de transaction est centralisee dans `app/crud.py`.

Lors d'un virement :

1. l'API verifie que les deux comptes existent ;
2. l'API refuse un virement vers le meme compte ;
3. l'API refuse un montant nul ou negatif ;
4. l'API verifie que le compte emetteur a assez d'argent ;
5. le solde du compte emetteur est diminue ;
6. le solde du compte receveur est augmente ;
7. le moteur de risque calcule un score simple ;
8. la transaction est enregistree avec le statut `OK` ou `FLAGGED`.

## Modele de donnees

### Client

Table : `clients`

| Champ | Type | Description |
| --- | --- | --- |
| `id` | integer | Identifiant du client |
| `name` | string | Nom du client |
| `country` | string | Pays du client |
| `risk_score` | float | Score de risque du client |

### Account

Table : `accounts`

| Champ | Type | Description |
| --- | --- | --- |
| `id` | integer | Identifiant du compte |
| `balance` | float | Solde du compte |
| `client_id` | integer | Client proprietaire du compte |

### Transaction

Table : `transactions`

| Champ | Type | Description |
| --- | --- | --- |
| `id` | integer | Identifiant de la transaction |
| `from_account` | integer | Compte debite |
| `to_account` | integer | Compte credite |
| `amount` | float | Montant transfere |
| `timestamp` | datetime | Date de creation |
| `status` | string | `OK` ou `FLAGGED` |

## Endpoints

### Clients

Creer un client :

```http
POST /clients/
```

Body :

```json
{
  "name": "Alice Martin",
  "country": "FR"
}
```

Lister les clients :

```http
GET /clients/
```

### Comptes

Creer un compte :

```http
POST /accounts/
```

Body :

```json
{
  "client_id": 1,
  "balance": 5000
}
```

Regles :

- `balance` doit etre superieur ou egal a `0` ;
- `client_id` doit correspondre a un client existant.

Lister les comptes :

```http
GET /accounts/
```

### Transactions

Creer une transaction :

```http
POST /transactions/
```

Body :

```json
{
  "from_account": 1,
  "to_account": 2,
  "amount": 250
}
```

Regles :

- `amount` doit etre strictement positif ;
- les deux comptes doivent exister ;
- le compte emetteur doit avoir assez d'argent ;
- `from_account` et `to_account` doivent etre differents.

Lister les transactions :

```http
GET /transactions/
```

## Moteur de risque

Le moteur de risque est defini dans `service/risk_engine.py`.

Fonction principale :

```python
check_transaction_risk(amount, client_history_count)
```

Regles actuelles :

| Condition | Risque ajoute |
| --- | --- |
| Montant superieur a `10000` | `+50` |
| Historique client inferieur a `5` transactions | `+20` |
| Montant superieur a `50000` | `+100` |

La transaction est marquee `FLAGGED` si le score final est superieur a `50`.

## Validation et erreurs

L'API retourne des erreurs HTTP explicites :

| Cas | Code |
| --- | --- |
| Client introuvable | `404` |
| Compte introuvable | `404` |
| Fonds insuffisants | `400` |
| Montant invalide | `422` ou `400` |
| Virement vers le meme compte | `400` |

FastAPI et Pydantic gerent automatiquement une partie des erreurs de validation, par exemple un montant negatif envoye a `POST /transactions/`.

## Verification rapide

Verifier la syntaxe et l'import de l'application :

```bash
make check
```

Afficher les routes disponibles :

```bash
make routes
```

## Production readiness

Le projet est structure pour evoluer vers une application plus robuste, mais les points suivants doivent etre traites avant une vraie production.

### Configuration

- Remplacer SQLite par PostgreSQL ou une base geree.
- Sortir toute configuration sensible dans des variables d'environnement.
- Desactiver `allow_origins=["*"]` en production.
- Ajouter un fichier `.env.example`.

### Base de donnees

- Ajouter Alembic pour les migrations.
- Ne pas versionner les fichiers `.db`.
- Ajouter des contraintes SQL explicites lorsque necessaire.
- Ajouter une strategie de sauvegarde.

### Securite

- Ajouter une authentification.
- Ajouter des roles et permissions.
- Ajouter une limitation de debit sur les routes sensibles.
- Valider plus strictement les donnees metier.

### Qualite

- Ajouter des tests unitaires.
- Ajouter des tests d'integration API.
- Ajouter un formatteur comme `black` ou `ruff`.
- Ajouter une verification CI.

### Observabilite

- Ajouter des logs structures.
- Ajouter des endpoints de healthcheck.
- Surveiller les erreurs et les temps de reponse.

## Exemple de scenario complet

1. Initialiser la base :

```bash
make seed
```

2. Lancer l'API :

```bash
make run
```

3. Ouvrir Swagger :

```text
http://127.0.0.1:8000/docs
```

4. Lister les clients avec `GET /clients/`.

5. Lister les comptes avec `GET /accounts/`.

6. Creer une transaction avec `POST /transactions/`.

7. Verifier les soldes avec `GET /accounts/`.

8. Verifier l'historique avec `GET /transactions/`.

## Afficher les donnees

Cette section sert de point d'entree rapide pour visualiser ce que contient le projet.

### Afficher avec Swagger

Lancer l'API puis ouvrir :

```text
http://127.0.0.1:8000/docs
```

Utiliser ensuite :

- `GET /clients/` pour afficher les clients ;
- `GET /accounts/` pour afficher les comptes et les soldes ;
- `GET /transactions/` pour afficher les virements ;
- `POST /transactions/` pour creer un nouveau virement et voir son statut.

### Afficher avec curl

Clients :

```bash
curl http://127.0.0.1:8000/clients/
```

Comptes :

```bash
curl http://127.0.0.1:8000/accounts/
```

Transactions :

```bash
curl http://127.0.0.1:8000/transactions/
```

Creer une transaction :

```bash
curl -X POST http://127.0.0.1:8000/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"from_account": 1, "to_account": 2, "amount": 250}'
```

### Afficher directement la base SQLite

Ouvrir la base :

```bash
sqlite3 data/bank.db
```

Lister les tables :

```sql
.tables
```

Afficher les clients :

```sql
SELECT * FROM clients;
```

Afficher les comptes :

```sql
SELECT * FROM accounts;
```

Afficher les transactions :

```sql
SELECT * FROM transactions;
```

Afficher les transactions suspectes :

```sql
SELECT * FROM transactions WHERE status = 'FLAGGED';
```

### Affichage futur recommande

Pour une interface plus lisible les étapes que je recommanderai seraient:

- PowerBI pour une visualisation metier ; (Power BI est la plus accurate pour de la restitution Fiable et facile en termes de maintenance)
- Streamlit pour un dashboard Python simple ;
- une page frontend dediee si le projet devient une application complete. (Nécessiterait plus de travail et de mobilisation de personnel ... mais très pro !!)
