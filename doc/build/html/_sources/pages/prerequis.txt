
Installation
############

Voici la documentation d'installation de Forjme!.

La présente documentation détaille les manipulations à effectuer pour obtenir une installation 
en production de Forjme!

Celles-ci ont été effectuées sur les distributions Linux Ubuntu 12.04 et Linux Debian 6.

Pré-requis
**********
Voici une liste des pré-requis :

* Python 2.7

* Django 1.4.3

* Une base de données MySQL ou autre, supportée par Python - Django

* Driver de base de données pour Python

* Git >= 1.7 (non testé si version <) 

Installation des outils
***********************
Comme déjà évoqué, l'installation décrite ici utilise une base MySQL. 

Rien n'empêche d'utiliser un autre type de base (postgresql, sqlite3, oracle)

Installation de Python
======================
Normalement, Python est déjà installé sous Ubuntu. Vous pouvez le vérifier en tapant cette simple commande::
    
    python -V

Si python est installé, cette commande renverra ::

    Python 2.7.3

Si ce n'est pas le cas, un simple appel au gestionnaire de paquet est nécessaire::

    sudo apt-get install python

Installation de Django
======================
Nous allons installer Django depuis les sources.

1. Rendez-vous sur la page du projet : `https://www.djangoproject.com/download/ <https://www.djangoproject.com/download/>`_

2. Téléchargez la dernière version stable (ici la 1.4.3) en version tar.gz dans un répertoire temporaire
    
    wget https://www.djangoproject.com/download/1.4.3/tarball/

3. Extraire l'archive

    tar xzvf Django-1.4.3.tar.gz

4. Entrez dans le répertoire créé par l'archive
    
    cd Django-1.4.3

5. Lancez l'installeur

    sudo python setup.py install

Installation du driver MySQL pour Python
========================================
Notre application utilisera une base de données MySQL. 

Aussi, il est nécessaire d'installer la librairie pour Python ::

    sudo apt-get install python-mysqldb
    
Installation de Git
===================

Pour installer Git, un simple ::

    sudo apt-get install git
    
Passons maintenant à la suite : :doc:`installation`



