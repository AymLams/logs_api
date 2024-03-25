Vous voilà dans l'application "Logs API", qui permet d'interagir avec des logs stockés en local dans le dossier "Data Folder"
que vous aurez set préalablement dans le config.json.
API à votre disposition:
    - POST "/logs/": prends 2 paramètres: un fichier (JSON ou YML) et une variable log_format (Valeurs possibles : JSON ou YML)
                    Cette méthode permet d'ingérer dans un CSV en local les logs détectés dans votre fichier.

    - GET "/logs/": prend un paramètre obligatoire en entrée : log_format (Valeurs possibles : JSON, YML, XML, CSV)
                    On peut ajouter un filtrage sur différents critères:
                        * ip (public ou private)
                        * before_time
                        * after_time
                        * type (prends en paramètre une liste de type d'attaques)

    - DELETE "/logs/": Ne prend pas de paramètres en entrée.
                        Cette méthode permet de supprimer les logs stockés en local.

Requirements :
    Il est obligatoire d'avoir Python 3.11 > d'installé sur votre machine afin d'initier l'API.

Pour lancer votre API :
    - Checker que le fichier config.json soit adapté à vos besoins.
    - Installer les librairies python : python3 -m pip install -r requirements.txt
    - Lancer l'API: python3 src/bin/main.py -c /PATH/TO/config.json


Pour tester votre API :
    - Checker le fichier de configuration config_test.json
    - Lancer les tests via la ligne de commande : pytest

A noter :
    Actuellement quand vous lancer votre projet sans la configuration, cela lancera l'API avec la configuration config_test.json
    un travail va être à mener par la suite pour gérer cette partie là.