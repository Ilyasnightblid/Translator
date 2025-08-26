# Application de Traduction Multi-Fonctionnelle

## Introduction

Cette application Flask offre une solution complète de traduction avec une interface de tableau de bord moderne. Elle propose trois modes de traduction : vocale en temps réel, saisie de texte manuscrit, et traduction de fichiers avec glisser-déposer. L'application inclut un système d'authentification sécurisé, un historique complet des traductions, des statistiques détaillées, et la gestion de profil utilisateur avec upload de photo. Interface entièrement localisée en français avec thème sombre/clair.

## Fonctionnalités Principales

- ✅ **Traduction vocale** en temps réel avec Web Speech API
- ✅ **Traduction de texte manuscrit** avec interface dédiée
- ✅ **Traduction de fichiers** (.txt, .json) avec glisser-déposer
- ✅ **Historique complet** avec édition/suppression et export CSV
- ✅ **Statistiques utilisateur** détaillées
- ✅ **Authentification sécurisée** avec gestion de session
- ✅ **Profil utilisateur** avec upload de photo de profil
- ✅ **Thème sombre/clair** avec sauvegarde des préférences
- ✅ **Interface responsive** entièrement en français

## Prérequis

- **Python 3.9 ou supérieur**
- **pip** (gestionnaire de paquets Python)
- **Git** pour cloner le projet
- Navigateur web moderne avec support Web Speech API (Chrome/Edge recommandés)

## Installation Locale (Étape par Étape)

### 1. Cloner le Projet

```bash
git clone <URL_DU_PROJET>
cd <NOM_DU_DOSSIER>
```

### 2. Créer un Environnement Virtuel

**Pour Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Pour macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les Dépendances

L'application utilise les dépendances suivantes. Installez-les avec pip :

```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install WTForms==3.1.0
pip install Werkzeug==3.0.1
pip install psycopg2-binary==2.9.9
pip install Pillow==10.1.0
pip install googletrans==4.0.0rc1
pip install langdetect==1.0.9
pip install gunicorn==21.2.0
pip install python-dotenv==1.0.0
pip install email-validator==2.1.0
```

**Ou installez toutes les dépendances d'un coup:**

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-WTF WTForms Werkzeug psycopg2-binary Pillow "googletrans==4.0.0rc1" langdetect gunicorn python-dotenv email-validator
```

## Configuration de la Base de Données

L'application utilise **SQLite** par défaut pour le développement local, avec support PostgreSQL pour la production.

### Première Installation

1. **Initialiser la base de données** (première fois seulement):
   ```bash
   flask db init
   ```

2. **Créer la migration initiale**:
   ```bash
   flask db migrate -m "Initial migration"
   ```

3. **Appliquer les migrations**:
   ```bash
   flask db upgrade
   ```

### Migrations Futures

Lorsque vous modifiez les modèles de données :

```bash
flask db migrate -m "Description des changements"
flask db upgrade
```

## Configuration des Variables d'Environnement

Créez un fichier `.env` à la racine du projet (optionnel pour le développement local) :

```env
SESSION_SECRET=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///translation_app.db
```

## Lancement de l'Application

### Option 1: Serveur de Développement Flask

```bash
flask run
```

### Option 2: Serveur Gunicorn (Recommandé)

```bash
gunicorn --bind 127.0.0.1:5000 --reload main:app
```

### Option 3: Directement avec Python

```bash
python main.py
```

## Accès à l'Application

Une fois le serveur démarré, accédez à l'application dans votre navigateur :

**URL:** `http://127.0.0.1:5000` ou `http://localhost:5000`

## Structure du Projet

```
├── app.py                  # Configuration de l'application Flask
├── main.py                 # Point d'entrée de l'application
├── models.py               # Modèles de base de données (User, Translation)
├── forms.py                # Formulaires WTForms
├── routes.py               # Routes et logique métier
├── utils.py                # Fonctions utilitaires
├── migrations/             # Scripts de migration de base de données
├── static/                 # Fichiers statiques
│   ├── css/               # Styles CSS
│   ├── js/                # Scripts JavaScript
│   ├── images/            # Images par défaut
│   └── profile_photos/    # Photos de profil utilisateur
├── templates/             # Templates Jinja2
│   ├── base.html         # Template de base
│   ├── auth/             # Templates d'authentification
│   └── dashboard/        # Templates du tableau de bord
└── uploads/              # Fichiers uploadés par les utilisateurs
```

## Utilisation de l'Application

### 1. Inscription/Connexion

- Accédez à la page d'accueil
- Créez un compte ou connectez-vous avec des identifiants existants

### 2. Traduction Vocale

- Cliquez sur "Traduction Vocale" dans la sidebar
- Sélectionnez la langue cible
- Cliquez sur "Commencer l'enregistrement"
- Parlez dans votre microphone
- La traduction apparaît en temps réel

### 3. Traduction de Texte

- Accédez à "Traduction de Texte"
- Saisissez votre texte dans la zone de texte
- Sélectionnez la langue cible
- Cliquez sur "Traduire"

### 4. Traduction de Fichiers

- Allez dans "Traduction de Fichiers"
- Glissez-déposez un fichier .txt ou .json
- Ou cliquez pour parcourir et sélectionner un fichier
- Choisissez la langue cible
- La traduction s'affiche instantanément

### 5. Gestion du Profil

- Cliquez sur votre avatar en haut à droite
- Sélectionnez "Mon Profil"
- Modifiez vos informations personnelles
- Changez votre photo de profil
- Mettez à jour votre mot de passe

### 6. Historique et Statistiques

- **Historique**: Consultez, modifiez ou supprimez vos traductions
- **Export**: Téléchargez votre historique au format CSV
- **Statistiques**: Visualisez vos métriques d'utilisation

## Dépendances Complètes

### Dépendances Python Principales

| Package | Version | Description |
|---------|---------|-------------|
| Flask | 3.0.0 | Framework web principal |
| Flask-SQLAlchemy | 3.1.1 | ORM pour base de données |
| Flask-Migrate | 4.0.5 | Migrations de base de données |
| Flask-Login | 0.6.3 | Gestion des sessions utilisateur |
| Flask-WTF | 1.2.1 | Formulaires et protection CSRF |
| WTForms | 3.1.0 | Validation de formulaires |
| Werkzeug | 3.0.1 | Utilitaires WSGI et sécurité |
| psycopg2-binary | 2.9.9 | Adaptateur PostgreSQL |
| Pillow | 10.1.0 | Traitement d'images |
| googletrans | 4.0.0rc1 | API de traduction Google |
| langdetect | 1.0.9 | Détection automatique de langue |
| gunicorn | 21.2.0 | Serveur WSGI de production |
| python-dotenv | 1.0.0 | Gestion des variables d'environnement |
| email-validator | 2.1.0 | Validation des emails |

### Dépendances Frontend

- **Bootstrap 5.3.0**: Framework CSS responsive
- **Font Awesome 6.4.0**: Icônes
- **Web Speech API**: Reconnaissance vocale (navigateur)

## Dépannage

### Problèmes Courants

1. **Erreur "Module not found"**
   ```bash
   # Vérifiez que l'environnement virtuel est activé
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\Activate.ps1  # Windows
   
   # Réinstallez les dépendances
   pip install --upgrade pip
   pip install <package_manquant>
   ```

2. **Erreur de base de données**
   ```bash
   # Supprimez la base de données et recréez-la
   rm instance/translation_app.db  # ou le fichier .db
   flask db upgrade
   ```

3. **Problème de permissions sur les fichiers uploadés**
   ```bash
   # Créez les dossiers nécessaires
   mkdir -p uploads static/profile_photos
   chmod 755 uploads static/profile_photos
   ```

4. **Le thème sombre ne fonctionne pas**
   - Vérifiez que JavaScript est activé dans votre navigateur
   - Ouvrez les outils de développement (F12) pour voir les erreurs
   - Effacez le cache du navigateur

5. **Upload de photos ne fonctionne pas**
   - Vérifiez que le dossier `static/profile_photos` existe et est accessible en écriture
   - Formats supportés: JPG, JPEG, PNG, GIF (max 16MB)

### Logs de Débogage

Pour activer les logs détaillés :

```bash
export FLASK_DEBUG=1
export FLASK_ENV=development
flask run
```

## Support et Contribution

### Signaler un Bug

Si vous rencontrez un problème :

1. Vérifiez que vous utilisez la dernière version
2. Consultez la section Dépannage
3. Vérifiez les logs d'erreur dans le terminal
4. Ouvrez une issue avec les détails suivants :
   - Version de Python utilisée
   - Système d'exploitation
   - Étapes pour reproduire le bug
   - Messages d'erreur complets

### Structure de l'Application

- **Backend**: Flask avec architecture en blueprints
- **Frontend**: Templates Jinja2 avec Bootstrap et JavaScript vanilla
- **Base de données**: SQLAlchemy ORM avec migrations Flask-Migrate
- **Authentification**: Flask-Login avec hashage sécurisé des mots de passe
- **Sécurité**: Protection CSRF, validation des uploads, sessions sécurisées

## Déploiement en Production

### Variables d'Environnement Requises

```env
SESSION_SECRET=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
FLASK_ENV=production
```

### Commande de Déploiement

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

## Licence

Ce projet est développé à des fins éducatives et de démonstration.

---

**Version**: 2.0.0
**Dernière mise à jour**: Août 2025

Pour toute question ou assistance, consultez la documentation ou contactez l'équipe de développement.