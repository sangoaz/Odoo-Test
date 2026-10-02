# Odoo Community – environnement Docker et module personnalisé

Projet d'apprentissage : mise en place d'un environnement Odoo 18 Community conteneurisé, développement d'un module qui étend les commandes de vente, et script d'intégration externe via l'API XML-RPC d'Odoo.

## Objectifs

- Déployer Odoo et PostgreSQL avec Docker Compose, avec un dossier d'addons monté pour le développement.
- Étendre un modèle natif (`sale.order`) sans modifier le code d'Odoo, par héritage.
- Ajouter des champs, un champ calculé stocké, une contrainte de validation et une vue héritée.
- Lire les données d'Odoo depuis un programme Python externe.

## Structure du dépôt

```
.
├── docker-compose.yml
├── addons/
│   └── sale_info_kevin/
│       ├── __init__.py
│       ├── __manifest__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── sale_order.py
│       └── views/
│           └── sale_order_views.xml
├── scripts/
│   └── xmlrpc_demo.py
└── README.md
```

## Prérequis

- Docker et Docker Compose
- Python 3.10+ (uniquement pour le script d'intégration)

## Lancement

```bash
docker compose up -d
```

Odoo est ensuite disponible sur http://localhost:8069. À la première connexion, créer une base (par exemple `test`) en cochant les données de démonstration, puis installer l'application **Ventes**.

Pour suivre les logs :

```bash
docker compose logs -f odoo
```

## Installation du module

1. Activer le mode développeur (Paramètres, en bas de page).
2. Dans **Applications**, cliquer sur « Mettre à jour la liste des applications ».
3. Rechercher `sale_info_kevin` et l'installer.

Après une modification du code Python, redémarrer le serveur (`docker compose restart odoo`). Après une modification d'un fichier XML, mettre à jour le module depuis le menu Applications.

## Fonctionnalités du module `sale_info_kevin`

| Élément          | Type                    | Rôle                                                                      |
| ---------------- | ----------------------- | ------------------------------------------------------------------------- |
| `priorite`       | `Selection`             | Niveau de priorité de la commande (normale / urgente)                     |
| `nb_articles`    | `Float` calculé, stocké | Somme des quantités des lignes de commande, recalculée via `@api.depends` |
| `_check_urgence` | `@api.constrains`       | Interdit une commande urgente de plus de 100 articles                     |
| Vue héritée      | `ir.ui.view` + `xpath`  | Affiche les deux champs sous le client dans le formulaire de commande     |

Choix techniques :

- **Héritage par `_inherit`** plutôt que modification du module `sale`, pour que le module reste compatible avec les mises à jour d'Odoo.
- **`store=True`** sur le champ calculé, pour pouvoir le filtrer, le trier et le lire via l'API sans recalcul à chaque accès.
- Aucun fichier `ir.model.access.csv` n'est nécessaire, car le module n'ajoute pas de nouveau modèle : il hérite des droits de `sale.order`.

## Script d'intégration

`scripts/xmlrpc_demo.py` s'authentifie auprès d'Odoo et lit les commandes confirmées, y compris le champ `nb_articles` ajouté par le module.

Les identifiants sont lus depuis des variables d'environnement, pour ne pas les écrire dans le code :

```bash
export ODOO_URL=http://localhost:8069
export ODOO_DB=test
export ODOO_USER=admin
export ODOO_PASSWORD=votre_mot_de_passe
python scripts/xmlrpc_demo.py
```

## Pistes d'amélioration

- Ajouter des tests unitaires avec `odoo.tests.TransactionCase`.
- Créer un nouveau modèle avec ses droits d'accès (`security/ir.model.access.csv`).
- Exposer un endpoint via un contrôleur `http.route` pour recevoir des webhooks.
- Ajouter un reverse proxy Nginx devant Odoo.
