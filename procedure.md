

# Déploiement Django sur Raspberry Pi 4 – Checklist

## 1. Préparation du projet Django

* [ ] Créer un projet Django localement ou cloner ton dépôt :

```bash
git clone https://github.com/ton-projet.git
cd ton-projet
```

* [ ] Créer un environnement virtuel Python :

```bash
python3 -m venv venv
source venv/bin/activate
```

* [ ] Installer les dépendances :

```bash
pip install -r requirements.txt
```

* [ ] Vérifier que le projet fonctionne en local :

```bash
python manage.py runserver
```

---

## 2. Installer le système et les dépendances sur le Raspberry Pi

* [ ] Mettre à jour le système :

```bash
sudo apt update && sudo apt upgrade -y
```

* [ ] Installer Python, pip, Git, Nginx et PostgreSQL :

```bash
sudo apt install python3-pip python3-venv git nginx postgresql postgresql-contrib libpq-dev -y
```

---

## 3. Configurer les fichiers statiques avec WhiteNoise

* [ ] Installer WhiteNoise :

```bash
pip install whitenoise
```

* [ ] Modifier `settings.py` :

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # autres middlewares...
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

* [ ] Collecter les fichiers statiques :

```bash
python manage.py collectstatic
```

---

## 4. Configurer les variables d’environnement

* [ ] Installer `django-environ` :

```bash
pip install django-environ
```

* [ ] Créer un fichier `.env` à la racine du projet :

```
SECRET_KEY=ta_super_clef
DEBUG=False
ALLOWED_HOSTS=192.168.1.42,localhost
DATABASE_URL=postgres://pi:motdepasse@localhost:5432/nom_de_ta_db
```

* [ ] Ajouter `.env` à `.gitignore` :

```
.env
```

* [ ] Modifier `settings.py` pour lire les variables d’environnement :

```python
import environ, os
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
CSRF_TRUSTED_ORIGINS = ["http://192.168.1.42", "http://localhost"]
DATABASES = {'default': env.db()}
```

---

## 5. Configurer PostgreSQL

* [ ] Créer la base et l’utilisateur :

```bash
sudo -u postgres psql
CREATE DATABASE myproject;
CREATE USER pi WITH PASSWORD 'motdepasse';
ALTER ROLE pi SET client_encoding TO 'utf8';
ALTER ROLE pi SET default_transaction_isolation TO 'read committed';
ALTER ROLE pi SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myproject TO pi;
\q
```

* [ ] Installer le driver PostgreSQL pour Python :

```bash
pip install psycopg[binary]
```

---

## 6. Installer et configurer Gunicorn

* [ ] Installer Gunicorn :

```bash
pip install gunicorn
```

* [ ] Tester Gunicorn :

```bash
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

---

## 7. Configurer Nginx comme reverse proxy

* [ ] Créer le fichier `/etc/nginx/sites-available/myproject` :

```
server {
    listen 80;
    server_name 192.168.1.42;

    location /static/ {
        alias /home/pi/ton-projet/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

* [ ] Activer le site et redémarrer Nginx :

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

---

## 8. Faire tourner Gunicorn en service systemd

* [ ] Créer `/etc/systemd/system/gunicorn.service` :

```
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/ton-projet
ExecStart=/home/pi/ton-projet/venv/bin/gunicorn --workers 3 --bind unix:/home/pi/ton-projet/gunicorn.sock myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

* [ ] Démarrer et activer le service :

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## 9. Vérifications finales

* [ ] Accéder au site via navigateur :
  `http://192.168.1.42`
* [ ] Vérifier que les fichiers statiques s’affichent correctement.
* [ ] Vérifier que la base PostgreSQL fonctionne.
* [ ] Vérifier que Gunicorn redémarre automatiquement après reboot du Pi.

---

## ✅ Résultat final : Architecture

```
[Browser] → [Nginx :80] → [Gunicorn] → [Django app]
                         ↑
                         [PostgreSQL local]
                         [Static files via WhiteNoise]
                         [Secrets via .env]
```

---

Si tu veux, je peux te faire **une version “copier-coller terminal”**, avec toutes les commandes exactes à exécuter **dans le bon ordre** pour déployer ton projet Django sur le Pi en une seule fois.

Veux‑tu que je fasse ça ?
