# Cyber Croc

Cyber Croc est une application web développée en Flask qui permet aux utilisateurs de créer des devis pour des solutions de cybersécurité, de gérer leurs comptes, et pour les administrateurs de gérer les utilisateurs et les devis. Les employés peuvent également voir les devis qui leur sont attribués et mettre à jour leur statut.

## Fonctionnalités

- **Inscription et Connexion des Utilisateurs**
- **Création et Gestion des Devis**
- **Tableau de Bord Administrateur**
  - Gestion des utilisateurs
  - Attribution des devis aux employés
  - Mise à jour des statuts des devis et ajout de commentaires
- **Gestion des Comptes Utilisateurs**
- **Vue Employé**
  - Visualisation des devis assignés

## Prérequis

- Python 3.7 ou plus
- Flask
- Flask-SQLAlchemy

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/ciscoderm/cyber-croc.git
    cd cyber-croc
    ```

2. Configurez la base de données :
    ```bash
    python3
    ```
    ```python3
    from app import app
    from models import db

    with app.app_context():
      db.create_all()
    ```

## Utilisation

1. Exécutez l'application Flask :
    ```bash
    flask run
    ```

2. Ouvrez votre navigateur et allez à `http://127.0.0.1:5000`.

## Gestion des Utilisateurs

### Ajouter un Administrateur

Pour ajouter un administrateur, utilisez le script `create_users.py` :
```bash
python create_admin.py
```
### ATTENTION
Si vous modifiez certaines choses, il ne faut pas oublier de supprimer le fichier app.db et refaire ce que la tache 2 nous demande, pour relancer une base donnée saine et vide.
