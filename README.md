# Learning FastAPI

## Besoin fonctionnel

On souhaite implémenter un service permettant la manipulation de logs de formats différents.

L'API, développée en `Python`, permettra de stocker des logs, de les consulter ou de les supprimer selon différents critères de filtrage.

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
A la suite du test, le candidat sera reçu lors d'un entretien de restitution où il devra présenter son code, ainsi que l'ensemble de ses choix techniques. Ces choix techniques seront débattu avec l'ensemble de l'équipe technique présente côté TEHTRIS.

Il sera demandé au candidat le temps réel passé sur le test.

Le candidat pourra également proposer un ensemble d'amélioration à l'application s'il avait eu plus de temps à sa disposition.
