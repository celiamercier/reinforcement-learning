# Le jeu des allumettes

Ce programme entraîne une IA au jeu des allumettes et permet d'en mesurer les performances.

## Règles du jeu
Le jeu démarre avec un certain nombre d'allumettes. Chacun leur tour, les joueurs peuvent retirer 1, 2 ou 3 allumettes. Le joueur qui prend la dernière allumette a perdu.
Il s'agit d'un jeu déterministe : il existe une stratégie gagnante pour le joueur qui joue en premier. C'est cette stratégie que l'IA doit apprendre par elle-même.

## Utilisation
Ce programme nécessite :
 - Python 3.xx
 - Matplotlip

#### Lancer le programme

    python matchsticks.py

Il vous sera demandé un certain nombre d'information permettant de paramétrer le programme :
 - Le nombre d'allumettes
 - Le nombre de parties d'entraînement
 - Le nombre de parties de test contre une IA aléatoire
 - La valeur de epsilon Ɛ
 - La valeur du learning rate μ
 - La valeur de gamma γ
 - L'affichage ou non de l'évolution de la value function

Le programme effectuera tout d'abord l'entraînement, puis le test de l'IA entraînée, et enfin vous permettra de jouer contre celle-ci.

#### Lancer le programme en mode debug

    python matchsticks.py debug

En mode debug le programme produira un fichier debug-{date}.log contenant pour chaque partie les actions prises par les deux joueurs ainsi que les valeurs de la value function avant et après entraînement. Il fixe également une seed, ce qui permet à chaque exécution d'avoir exactement le même déroulement.

## Entraînement
#### Apprentissage
L'entraînement utilise la définition de la **Q-function**, soit l'espérance de gain de choisir une action à partir d'un certain état donné. Un état ici correspond au nombre d'allumettes restantes.

La formule d'apprentissage est la suivante :

    Q(s,a) = Q(s,a) + μ(R - Q(s,a)) si a est la dernière action prise
    Q(s,a) = Q(s,a) + μ(R + γ*maxQ(s',a') - Q(s,a)) sinon

Où :
 - *Q(s,a)* correspond à la valeur de la Q-function pour l'action *a* prise à l'état *s*
 - *maxQ(s',a')* correspond à la valeur de la Q-function pour l'action *a'* maximisant Q depuis l'état *s'* suivant *s*
 - *μ* correspond au learning rate
 - *γ* correspond au facteur gamma
 - *R* correspond à la récompense obtenu

#### Prise de décision
Lors de l'entraînement, l'IA va faire un choix entre **exploration** (action aléatoire) et **exploitation** (action optimale), en se basant sur la valeur de Ɛ. Celle-ci décroit au fur et à mesure de l'entraînement afin de progressivement faire émerger la stratégie optimale.

    Si rand() < Ɛ alors random_action()
    Sinon greedy_action()

Les phases d'exploitation consistent à prendre la décision maximisant la Q-function, soit maximisant l'espérance de gain.
