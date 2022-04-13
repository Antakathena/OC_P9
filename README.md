# OC_P9

## Study Project : Django Training. Web app creation

### Infos Générales :
OC_P9 est un programme d'étude du Framework python Django (MVT).

### Utilité :
Il s'agit d'une app web qui permet aux utilisateurs connectés de demander des critiques de livre et d'en poster.


### Fonctionnalités :
#### Le Projet se nomme LIReview, il est dans un fichier nommé src et comporte deux app : users et reviews.

#### Un utilisateur peut :
    - se connecter et s'inscrire (une app "users" distincte, le reste se trouve dans l'app "reviews")
    - acceder à son profil, ajouter ou modifier des informations (app "users")

    - consulter un flux contenant les tickets et commentaires des utilisateurs qu'il suit, classés par ordre antéchronologique.(page feed/Accueil si connecté)
    - créer de nouveaux tickets pour demander une critique (depuis feed ou Mes Posts)
    - créer une critique en réponse à un ticket (depuis feed ou Mes Posts)
    - créer une critique sans ticket, générant en même temps le ticket correspondant (depuis créer une critique, vue review_plus_ticket)
    - voir, modifier et supprimer ses propres tickets et commentaires (page Mes Posts)
    - choisir de suivre d'autres utilisateurs ou ne plus les suivre


#### Organisation (détail et remarques sur l'app reviews):

    models.py :
        - Ticket
        - Review
        - Userfollows

    views.py :
        - les vues connect et review_plus_ticket sont des Function Based Views,

        - les autres sont des Class Based Views (CBV) :
            . pour les modèles Ticket et Review : Detail, Create, Update, Delete Views,
                et templates correspondants
            . pour le modèle UserFollows : CreateView et DeleteView

        - les vues FeedListView et MyPostListViews sont des CBV de type ListViews,
                leurs méthodes servent à assembler les tickets et les reviews
                pour les pages Feed (Accueil) et Mes Posts



### Instruction de démarrage :
Dans un terminal, utiliser les commandes suivantes :

$ python3 -m venv env (créé un dossier env dans le répertoire où vous vous trouvez)

$ source env/bin/activate (sous linux) ou env\Scripts\activate.bat (pour activer l'environnement virtuel sous windows)

$ git clone https://github.com/Antakathena/OC_P9

$ cd ../chemin/du/dossier (de la copie de OC_P9 dans votre dossier env)

$ pip install -r requirements.txt

$ cd src

Une fois dans le dossier src, utiliser la commande 

$ python manage.py runserver

Vous pourrez alors explorer localement l'app
sur votre navigateur à l'adresse http://127.0.0.1:8000/

### Informations supplémentaires :
- Python 3.10 a été utilisé pour ce projet.

- Front : Pour le CSS le framework Bootstrap a été utilisé (classes Bootstrap dans le HTML)
    et une feuille de style style.css + resermeyer.css qui sert à neutraliser 
    les informations de mise en page inhérentes au HTML pour éviter certains soucis.

- Des exemples de reviews, tickets et users sont fournis dans la base de donnée (db.squlite3),
    Mot de passe des utilisateurs tests : Testing321  
