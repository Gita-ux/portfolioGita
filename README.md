# Portfolio – Watio Gita (Django)

## Lancer le site
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac : source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed          # contenu de départ (modifiable ensuite)
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```
- Site : http://127.0.0.1:8000
- Administration : http://127.0.0.1:8000/admin
- Test sur téléphone (même WiFi) : http://IP_DE_TON_PC:8000

## Personnaliser (tout se fait dans /admin)
- **Profil** : photo, CV (PDF), textes, contacts, réseaux sociaux
- **Compétences** : ajuste les niveaux (%) selon ta réalité
- **Projets** : ajoute images, liens, catégorie (Réseaux, Web, Mobile, Design)
- **Parcours** : stages et formations
- **Messages reçus** : messages du formulaire de contact

## Couleurs (core/static/core/css/style.css, haut du fichier)
Variables `--grad`, `--violet`, `--orange` pour changer le dégradé.
Le thème sombre est le thème par défaut ; le choix clair/sombre est mémorisé.

## Avant la mise en ligne
Dans config/settings.py : `DEBUG = False`, nouvelle `SECRET_KEY`, `ALLOWED_HOSTS`
avec ton domaine, puis `python manage.py collectstatic`.
