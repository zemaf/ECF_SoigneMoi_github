# SoigneMoi


---

## Déploiement local d'une application Django

### Prérequis
- Python installé sur votre machine (version 3.x recommandée)
- pip (gestionnaire de paquets Python)

### Étapes de déploiement

1. **Cloner le dépôt**
   
   Commencez par cloner le dépôt GitHub contenant votre application Django sur votre machine locale.
   ```
   git clone https://github.com/zemaf/SoigneMoi.git
   cd SoigneMoi
   ```

2. **Créer un environnement virtuel**
   
   Il est recommandé de créer un environnement virtuel pour isoler les dépendances de votre projet.
   ```
   python -m venv env
   ```
   
   Activez l'environnement virtuel :
   - Sur Windows : `env\Scripts\activate`
   - Sur Unix ou MacOS : `source env/bin/activate`

3. **Installer les dépendances**
   
   Installez toutes les dépendances nécessaires à partir du fichier `requirements.txt`.
   ```
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   
   Si votre projet utilise des variables d'environnement (par exemple, des secrets de base de données, des clés API), assurez-vous de les configurer. Vous pouvez les définir manuellement dans votre environnement ou utiliser un fichier `.env` que Django peut charger avec `django-environ`.

5. **Appliquer les migrations**
   
   Appliquez les migrations de la base de données pour initialiser ou mettre à jour la structure de votre base de données.
   ```
   python manage.py migrate
   ```

6. **Collecter les fichiers statiques (si nécessaire)**
   
   Si votre application utilise des fichiers statiques, exécutez la commande suivante pour les collecter dans le dossier spécifié par `STATIC_ROOT`.
   ```
   python manage.py collectstatic
   ```

7. **Lancer le serveur de développement**
   
   Vous pouvez maintenant lancer le serveur de développement Django pour accéder à votre application localement.
   ```
   python manage.py runserver
   ```
   Par défaut, le serveur tournera à l'adresse `http://127.0.0.1:8000/` dans votre navigateur.

### Accéder à l'application

Ouvrez votre navigateur et allez à l'adresse `http://127.0.0.1:8000/` pour voir votre application en action.

---

