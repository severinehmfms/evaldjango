
# Titre : Evaluation Web Python - Framework Django

# Sujet : Echange de compétences

## Auteur : Séverine Hori Maitrehut

### Description : 
Il s'agit de spécifier, concevoir et réaliser le prototype d'un système qui permettrait à des personnes d'échanger des compétences (ex. : jardinage, administration d'un ordinateur), permettant d'accomplir des activités (ex. : tailler un rosier, installer un logiciel), avec des personnes près d'elles, à des créneaux leur convenant, et en tenant compte de la météo si certaines activités en dépendent.
Ce prototype est une application Web, qui n’intégrera pas – dans cette première version demandée pour cette évaluation – la recherche de proximité des personnes, ni l’utilisation de la météo pour savoir si un créneau est favorable à une activité et considérera qu’un créneau est une journée entière (à l’intérieur de laquelle on suppose que les personnes peuvent convenir d’un créneau pour se rencontrer).

### Versions
Version de python : 3.14
Version de django : 5.2.18

### Installation : 
- Cloner le répertoire git
- Créer un environnement virtuel pour ce projet, et l'activer
- Se placer dans le répertoire **biaudentraide** 
- Réinstaller les dépendances en lançant cette commande de votre terminal :
	*python -m pip install -r requirements.txt*
- Effectuer les migrations de la base de données du projet 
	*python manage.py migrate*
	