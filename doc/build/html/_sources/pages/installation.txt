
Installation de Forjme!
#######################

Pour l'instant, il n'existe pas de paquet de Forjme! pour distribution, mais l'installation depuis
les sources est tellement triviale que les paquets seront pour plus tard.

Note:
"""""
Toute l'installation de Forjme! sera réalisée dans le répertoire /home/forjme (le home de l'utilisateur forjme).

Clonage des sources
*******************

Les sources de Forjme sont sur la plateforme Github.

Clonons-les via un simple ::

   cd /home/forjme
   git clone https://github.com/gbtux/forjme.git
   
Un répertoire "forjme" a dû être créé.

Mis à part les pré-requis, c'est la seule installation nécessaire !

Passons maintenant à la configuration.

Configuration
*************
La configuration de forjme est centralisée dans un seul fichier : **settings.py**

Voici le détail des paramètres à initialiser, il y en a d'autres, 
mais ils ne sont pas nécessaires à notre configuration, ou il faut laisser le paramètre par défaut.

En cas de doute, laissez le paramètre par défaut, et voyez ce que Django vous dit !

Niveau de debug
===============

Les deux paramètres sont à configurer comme suit : ::

   DEBUG = False
   TEMPLATE_DEBUG = DEBUG

DEBUG est à True par défaut

Base de données
===============

La configuration de la base de données par défaut : ::

   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'forjme',                      # Or path to database file if using sqlite3.
        'USER': 'forjme',                      # Not used with sqlite3.
        'PASSWORD': 'forjme',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
   }
  
Timezone
========
Configuration de la zone horaire : ::

   TIME_ZONE = 'Europe/Paris'
   
Si ce n'est pas la vôtre, vous pouvez trouver une liste des timezone sur Wikipédia `ici <http://en.wikipedia.org/wiki/Lists_of_time_zones>`_

Langue
======

Configuration de la langue : ::

   LANGUAGE_CODE = 'fr-fr'
   
Comme pour les timezone, consultez la page de référence `ici <http://www.i18nguy.com/unicode/language-identifiers.html>`_


Media path
==========
Ce paramètre est utilisé pour indiquer le chemin **absolu** du répertoire média.

Indiquez ici le chemin complet : ::

   MEDIA_ROOT = '/home/forjme/forjme/media/'
   
Media URL
=========
De même que le chemin vers les medias, il est nécessaire d'indiquer à Django la fin d'URL à utiliser pour le répertoire de média.

Par défaut (cf configuration Apache) : ::

   MEDIA_URL = '/media/'
   

Clé de hashage
==============
Cette clé est utilisée dans plusieurs algorithmes cryptographiques de Django (Token CSRF, ...).

Elle est d'une longueur de 50 caractères maximum : ::

   SECRET_KEY = 'pmo4*m&amp;il+9(fh+$ve&amp;e1mkue=#(@phh%h(o1x5)=q#^+7#%e@'

Vous pouvez utiliser ce générateur sur `le web <http://www.miniwebtool.com/django-secret-key-generator/>`_


Envoi de mail
=============
Pour envoyer des notifications, Forjme! utilise un serveur SMTP. 

Celui de votre entreprise, ou de votre F.A.I fera très bien l'affaire.

Par défaut, la configuration est positionnée sur une adresse Gmail : ::

   EMAIL_USE_TLS = True
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_HOST_USER = 'openlvb.project@gmail.com'
   EMAIL_HOST_PASSWORD = '??'
   EMAIL_PORT = 587   
   
Si vous avez des doutes, il s'agit souvent de desactiver le TLS, et d'utiliser le port 25 de votre serveur SMTP pour trouver la bonne configuration.

Paramètres FORJME
=================
Seuls 2 paramètres spécifiques à Forjme! sont à positionner :

* FORJME_ARCHIVE_DIR : répertoire de création d'une archive de projet (fichier temporaire). A laisser tel.

* FORJME_GIT_ROOT : c'est **LE** répertoire à configurer pour accéder à la racine de vos repos GIT (ne pas oublier le / de fin).

Si vous n'avez pas encore créé de repository Git, ou ne reprenez pas d'existant, crééz un répertoire où bon vous semble.

Ce répertoire sera le répertoire dans lequel seront créés les repository.

Dans tous les cas, ce répertoire créé devra avoir les droits positionnés en lecture / écriture pour l'utilisateur Apache.

 


 

