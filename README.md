# Test Technique - SIEM

## Conditions de réalisation

* Candidat: Developpeur Python
* Durée: ∼4h
* Temps de réalisation: 72h
* Langage: Python 3.11 ou supérieur (https://www.python.org/)
* Framework: FastAPI (https://fastapi.tiangolo.com/)
* Langue: Anglais

La durée notée ne représente ni une durée réelle du test, ni une borne maximale de temps, elle correspond a une estimation du temps que l'on attend du candidat pour réaliser le plus possible de développement.

## Besoin fonctionnel

On souhaite implémenter un service permettant la manipulation de logs de formats différents.

L'API, développée en `Python`, permettra de stocker des logs, de les consulter ou de les supprimer selon différents critères de filtrage.

TEHTRIS a besoin de vous pour mettre en place cette fonctionnalité de bout en bout.

## Spécifications techniques

### Format des logs

Il existe deux formats de logs:

* JSON (fichier `.json`)
* YAML (fichier `.yaml`)

Les paires clef/valeur du log sont indépendantes du format et sont normalisées et typées comme suit:

```plaintext
uid: str # un identifiant unique du log, sous la forme d'un uid
ip: str # une adresse IPv4 pouvant être publique ou privée
size: int # un entier naturel correspondant a la taille de la payload, non remontée dans ce test
time: datetime # un objet contenant la date et l'heure de génération du log
allow: bool # un booléen correspondant à l'état du log (s'il a été accepté ou non par le moteur)
type: list[str] # une liste contenant des types d'IoC détecté dans la payload
```

Il n'y a pas de clefs supplémentaires par rapport à celles indiquées ci-dessus.

Toutes ces clefs sont présentes dans tous les logs.

Les types d'IoC (Indice of Compromission) sont obtenus après analyse du log et permettent de déterminer si la payload initiale est malveillante. `type` peut donc conternir une ou plusieurs IoC.

Les différents types d'IoC peuvent être:

* "phishing"
* "malware"
* "exploit"
* "c2"
* "spam"

Un exemple de log au format `JSON` peut donc être:

```json
{
  "uid": "4a4f968a-102a-1006-80e4-6f312e703235",
  "ip": "127.0.0.1",
  "size": 10,
  "time": "2011-11-04T00:05:23",
  "allow": true,
  "type": [
    "phishing",
    "malware"
  ]
}
```
Notez que dans l'exemple ci-dessus, le log est en multi-ligne mais ce n'est pas nécessairement le cas.

Un exemple de ce même log au format `YAML`:

```yml
uid: 4a4f968a-102a-1006-80e4-6f312e703235
ip: 127.0.0.1
size: 10
time: 2011-11-04T00:05:23
allow: True
type:
  - phishing
  - malware
```

### Stockage des logs

Les logs devront être stockés sur disque dans un répertoire dédié défini dans le fichier de configuration ( `data_folder` ).

Un fichier de log contient un nombre maximum fixe de log, ce maximum est également défini dans le fichier de configuration (`max_file_size`).

Si le fichier est plein, il faut en créer un nouveau pour stocker les logs.

### Spécifications de l'API

Le nommage de l'endpoint à utiliser pour la ou les routes qui permettent la manipulation de logs est laissé libre.

L'API possède trois méthodes distinctes à implémenter:

* GET: récupère 0 à `n` logs matchant différents critères
* POST: sauvegarde 1 à `n` logs
* DELETE: supprime tous les logs

**GET:**

* La méthode permet de renvoyer 0 à `n` logs
* Le format de sortie doit être défini par l'utilisateur via une clef `log_format` qui peut prendre la valeur d'un des formats acceptés dans la grammaire.
* Les logs obtenus dans le résultat de la méthode devront être récupérables dans un fichier dont l'extension correspond au format
* La méthode possède des critères de filtrage pour afficher les logs stockés correspondant à ces critères:
  * `ip`: filtre les logs en fonction de la nature de l'adresse IP. Valeurs possibles:
    * `private`: filtre tous les logs dont le champ `ip` correspond à une ip privée
    * `public`: filtre tous les logs dont le champ `ip` correspond à une ip publique
  * `before_time`: filtre les logs dont le champ `time` est \< `before_time`
  * `after_time`: filtre les logs dont le champ `time` est \> `after_time`
  * `type`:
    * Liste de 1 à `n` string présentes dans la liste des IoC ci-dessus
    * Les élements renseignés remplissent la condition d'Union. Ainsi si `type` = `['phishing', 'malware']`, le filtre renvoie les logs dont `type` = `phising` ou `type` = `malware`
    * Le filtre est case insensitive
* Tous les filtres décrits ci-dessus sont optionnels à l'utilisation. Un filtre non utilisé match tous les logs. Ex: renvoyer tous les logs avec des adresses IP publiques -\> tous les filtres sont laissés vides, excepté `ip` qui doit valoir `public`

**POST:**

* Prend en paramètre 1 fichier uniquement en entrée pouvant contenir 1 à `n` logs
* Le format d'entrée peut-être l'un des deux formats présentés dans la rubrique précédente: `JSON` ou `YAML`
* Le fichier peut être un `.json` ou `.yml` contenant respectivement un ou plusieurs logs au format `JSON` ou `YAML`
* Dans le `body` de la requête, on souhaite voir apparaitre le paramètre `log_format` qui peut prendre la valeur d'un des formats énoncés dans la grammaire
* Les autres formats de logs ou de fichiers ne sont pas acceptés par le moteur
* La méthode permet de sauvegarder les logs envoyés en local dans un fichier. On rappelle que la taille maximale d'un fichier est définie dans le fichier de configuration

**DELETE:**

* La méthode ne prend aucun paramètre et permet d'effectuer un reset pour rétablir l'état initial, c'est à dire, tout supprimer
* En plus de supprimer les logs, on souhaiterait que la méthode retourne le nombre de logs supprimés

Dans ce projet, l'authentification n'est pas a gérer.

### Configuration

Le code doit être configurable via un fichier de configuration `config.json`, contenant les variables suivantes:

```plaintext
data_folder: str # chemin du dossier qui contiendra les logs analysés par le service
max_file_size: int # nombre de log max accepté par fichier de log
api_address: str # API IP
api_port: int # API port
```

Le candidat peut ajouter des variables au fichier de configuration à condition que ces variables soient optionnelles pour l'exécution du programme.

## Bonus

Les bonus sont optionnels et requiert un temps de développement supplémentaire non négligeable. Ils sont à implémenter à l'appréciation du candidat et leur non implémentation ne rentrera pas en compte dans l'évaluation finale de l'exercice.

A défaut d'implémentation, vous pourrez évoquer vos idées de mise en oeuvre lors de l'entretien de restitution.

### Bonus 1

On souhaite compléter la méthode GET à l'aide de nouveaux filtres répondant aux critères suivants:

* `uid`: Filtre le log dont l'`uid` est renseigné, le filtre est case sensitive
* `max_size`: filtre les logs dont le champ `size` est \< `max_size`
* `min_size`: filtre les logs dont le champ `size` est \> `min_size`
* `allow`: Filtre le log selon la valeur du champ `allow`

On rappelle que tous les filtres sont optionnels lors d'une recherche.

### Bonus 2

Proposez une implémentation pour pouvoir ingérer les logs autrement que par la méthode `POST` en passant par une Websocket.

### Bonus 3

Un troisième format de log s'est ajouté à la grammaire. Il s'agit du format `TEHTRIS`, dont les logs sont stockés dans des fichiers d'extension `.log`, et dont le format est le suivant:

```plaintext
<165>1 2022-01-13T15:35:11 127.0.0.1 LOG - [4a4f968a-102a-1006-80e4-6f312e703235] - size:10 allow:true type:phishing type:malware
```

Le format `TEHTRIS` suit une RFC syslog approximative, dont le pattern correspond au format suivant:

```plaintext
<PRIORITY>VERSION %time% %ip% LOG - [%uid%] - MESSAGE
```

Où `MESSAGE` correspond à l'ensemble des paires clef/valeur manquantes:

```plaintext
size:%size% allow:%allow% type:%type%
```

L'odre des paires clef/valeur du champ `MESSAGE` n'est pas forcément celui affiché ci-dessus. En dehors du champ `MESSAGE`, l'ordre des champs est fixe. Les séparateurs clef/valeur sont des `:` et les séparateurs paires de clef/valeur sont des espaces.

Pour le champ `type`, s'il y a plusieurs valeurs, la clef peut apparaître plusieurs fois.

La priorité par défaut est 165 et la version par défaut est 1. De manière générale, ces deux champs sont toujours présent dans les logs format `TEHTRIS` et sont maintenant optionnels dans les logs format `JSON` et `YAML`.

On souhaite que ce format de log soit maintenant compatible avec l'API. Cela implique qu'il faut modifier les routes `GET` et `POST` en conséquence.

## Fichiers fournis au candidat

* `README.md`: un fichier contenant les instructions du test
* `config.json`: un fichier contenant des variables configurables à utiliser
* `examples/`: un dossier contenant un ensemble de fichiers de logs exemples
  * `single.json`: un fichier contenant un log au format JSON
  * `single.yml` : un fichier contenant un log au format YAML
  * `single.log` : un fichier contenant un log au format TEHTRIS
  * `multi.json`: un fichier contenant plusieurs logs au format JSON
  * `multi.yml` : un fichier contenant plusieurs logs au format YAML
  * `multi.log` : un fichier contenant plusieurs logs au format TEHTRIS

## Livrables

Il est attendu du candidat de fournir l'ensemble des livrables suivants au sein d'une archive `technical_test.tgz` contenant:

* Un fichier de `requirements.txt` contenant toutes les dépendances
* Un ou plusieurs fichiers de code en Python répondant aux spécifications techniques
* Un ou plusieurs fichiers de code contenant un ensemble de tests unitaires de l'application
* Un ou plusieurs fichiers de documentation

### Exécution

Attention, le rendu sera testé automatiquement ! Veillez à ce que les commandes suivantes puissent s'éxecuter sur votre rendu:

```bash
tar -xzf technical_test.tgz
cd technical_test/
python3 -m pip install -r requirements.txt
python3 src/bin/main.py -c /PATH/TO/config.json
```

## Critères d'évaluation

Le candidat sera évalué sur les critères suivants:

* Sa capacité à implémenter une API en Python
* Sa capacité à produire du code optimisé
* Sa capacité à utiliser les bibliothèques adéquates
* Sa capacité à tester son code
* Sa capacité à documenter ses productions

Il n’y a pas de bonne ou de mauvaise implémentation, l'attention sera portée tant sur le fond que la forme et la capacité du candidat à défendre ses choix techniques.

## Entretien de restitution

A la suite du test, le candidat sera reçu lors d'un entretien de restitution où il devra présenter son code, ainsi que l'ensemble de ses choix techniques. Ces choix techniques seront débattu avec l'ensemble de l'équipe technique présente côté TEHTRIS.

Il sera demandé au candidat le temps réel passé sur le test.

Le candidat pourra également proposer un ensemble d'amélioration à l'application s'il avait eu plus de temps à sa disposition.
