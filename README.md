
---

# Mob Blog

Mob Blog est une **application de blogging développée avec Django**, permettant aux utilisateurs de créer, éditer et supprimer des articles, ainsi que de commenter les articles des autres. Le projet est conçu pour la pratique professionnelle et le déploiement en production sur un serveur dédié.

---

## 🛠 Stack technique

* **Backend :** Django 4.x
* **Base de données :** PostgreSQL (en production) / SQLite (développement)
* **Serveur WSGI :** Gunicorn
* **Reverse Proxy :** Nginx
* **Static files :** WhiteNoise
* **Authentification :** Django `User` model + LoginRequiredMixin
* **Variables d’environnement :** django-environ / `.env`
* **Versioning / Déploiement :** Git / GitHub

---

## ⚡ Fonctionnalités principales

* **Articles**

  * Création, modification, suppression par l’auteur seulement.
  * Vue détaillée avec affichage du corps et des commentaires.
* **Commentaires**

  * Système de commentaires lié aux articles.
  * L’affichage et la soumission des commentaires se fait via des vues class-based séparées (`CommentGet` et `CommentPost`), combinées dans un wrapper `ArticleDetailView`.
* **Sécurité**

  * Gestion des utilisateurs avec `LoginRequiredMixin`.
  * Validation CSRF et protection des formulaires.
* **Administration**

  * Interface Django Admin pour la gestion des articles, commentaires et utilisateurs.

---

## 🏗 Architecture des vues

* `CommentGet` : GET → affichage article + formulaire commentaire.
* `CommentPost` : POST → traitement et sauvegarde des commentaires.
* `ArticleDetailView` : wrapper → délègue selon la méthode HTTP.

**Flux résumé :**

```
[Browser] → [Nginx :80] → [Gunicorn] → [Django app]
                         ↑
                         [PostgreSQL local]
                         [Static files via WhiteNoise]
                         [Secrets via .env]
```

---

## 💻 Installation locale

1. **Cloner le projet**

```bash
git clone https://github.com/ton-utilisateur/mob-blog.git
cd mob-blog
```

2. **Créer un environnement virtuel**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configurer `.env`**

```text
SECRET_KEY=ta_super_clef
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

4. **Lancer les migrations**

```bash
python manage.py migrate
python manage.py createsuperuser  # optionnel
```

5. **Lancer le serveur local**

```bash
python manage.py runserver
```

---

## 🚀 Déploiement sur serveur dédié (Raspberry Pi 4)

* Installer Python, PostgreSQL, Nginx sur le Pi.
* Configurer les variables d’environnement dans `.env`.
* Installer Gunicorn et le tester :

```bash
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

* Configurer Nginx pour servir les fichiers statiques et proxy vers Gunicorn.
* Mettre Gunicorn en service systemd pour démarrage automatique.
* Vérifier le site depuis le réseau local.

*(Voir le guide complet de déploiement dans `DEPLOYMENT.md` pour plus de détails.)*

---

## 📂 Structure du projet

```
mob-blog/
├── articles/              # App Django pour les articles et commentaires
├── users/                 # App Django pour la gestion des utilisateurs
├── templates/             # Templates HTML
├── static/                # Fichiers statiques
├── media/                 # Fichiers uploadés
├── manage.py
├── requirements.txt
├── .env                   # Variables d'environnement
└── README.md
```

---

## 🔑 Variables d’environnement

| Variable        | Description                                    |
| --------------- | ---------------------------------------------- |
| `SECRET_KEY`    | Clé secrète Django                             |
| `DEBUG`         | Mode debug (True/False)                        |
| `ALLOWED_HOSTS` | Liste d’hôtes autorisés                        |
| `DATABASE_URL`  | URL de la base de données PostgreSQL ou SQLite |

