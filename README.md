Plateforme d'Analyse de Vulnérabilité

Cette plateforme vous permet d'analyser la sécurité de vos sites web en utilisant des outils de vulnérabilité comme Nmap et OWASP ZAP. Elle est conçue pour fournir des rapports détaillés sur les vulnérabilités potentielles trouvées sur vos sites.
Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

    Python : Version 3.6 ou supérieure
    Nmap: $ sudo apt install nmap
    XAMPP MySQL : Assurez-vous que MySQL est installé et en cours d'exécution sur votre système.
    OWASP ZAP : Assurez-vous que OWASP ZAP est installé et configuré en mode daemon avec une clé API valide. 
        Utilise ceci comme api "rlminssppe06h577ks4m2c460k" tu pourras modifier ça dans Outils --> Option -->  API

Installation des Dépendances Python

Installez les bibliothèques Python nécessaires en exécutant la commande suivante :

bash

pip install mysql-connector-python python-owasp-zap-v2.4

Configuration de la Base de Données

    Créez une base de données MySQL nommée vulnerability_analysis.
    Configurez les tables nécessaires en utilisant les scripts SQL fournis dans le README.
    *
    CREATE TABLE nmap_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE owasp_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

*

Configuration d'OWASP ZAP

Assurez-vous que OWASP ZAP est en cours d'exécution en mode daemon avec l'API activée. Vous pouvez démarrer OWASP ZAP avec la commande suivante dans votre terminal :

bash

zap.sh -daemon -config api.key=rlminssppe06h577ks4m2c460k

Remplacez rlminssppe06h577ks4m2c460k par votre propre clé API OWASP ZAP.
Utilisation de la Plateforme

    Clonez ce dépôt Git sur votre machine locale.

    Configurez les paramètres dans les scripts Python (analyze.py et analyze_zap.py) :
        Assurez-vous que db_config dans server.py, analyze.py et analyze_zap.py est correctement configuré pour se connecter à votre base de données MySQL.
        Vérifiez que ZAP_API_KEY dans analyze_zap.py correspond à votre clé API OWASP ZAP.

    Exécutez le serveur Python en utilisant la commande suivante :

    bash

    python server.py

    Accédez à l'interface utilisateur en ouvrant votre navigateur web et en visitant http://localhost:8000.

    Soumettez l'URL du site web que vous souhaitez analyser dans le champ prévu.

    Consultez les rapports de vulnérabilité générés à partir des analyses de Nmap et d'OWASP ZAP sur la page résultante.

Structure du Projet

    server.py : Serveur HTTP Python utilisant http.server pour gérer les requêtes POST pour l'analyse des sites web.
    analyze.py : Script Python pour exécuter une analyse de vulnérabilité avec Nmap et enregistrer les résultats dans la base de données.
    analyze_zap.py : Script Python pour exécuter une analyse de vulnérabilité avec OWASP ZAP et enregistrer les résultats dans la base de données.
    index.html : Fichier HTML pour l'interface utilisateur permettant de soumettre les URL des sites web à analyser.
    style.css : Feuille de style CSS pour la mise en forme de l'interface utilisateur.
    report.html : Modèle HTML utilisé pour afficher les rapports de vulnérabilité générés.

Notes Additionnelles

    Assurez-vous que les ports nécessaires pour Nmap et OWASP ZAP sont accessibles depuis votre système.
    Les scripts fournis sont basés sur une configuration locale et peuvent nécessiter des ajustements pour un déploiement en production.
