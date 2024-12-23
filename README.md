# Guide de Lancement et d'Utilisation

## Description
Ce projet est une application interactive utilisant **Ingescape Circle V4** pour gérer un jeu en mode solo ou multijoueur. Ce fichier détaille les instructions pour installer, configurer et exécuter l'application.

## Prérequis
### Logiciel requis
- **Ingescape Circle V4**

### Librairies Python nécessaires
Les librairies suivantes sont requises :
- `pygame`
- `moviepy`
- `ingescape`
- `numpy`
- `PIL`
- `http.server`
- `socketserver`
- `pynput`

Ces dépendances sont listées dans le fichier `requirements.txt` à la racine du projet. Pour les installer, utilisez la commande suivante :
```bash
pip install -r requirements.txt
```

## Modes de Jeu

### Jeu Solo
1. Ouvrez le projet dans **Ingescape Circle V4**.
2. Connectez-vous au réseau Wi-Fi **5670**. Le logiciel Circle doit ressembler à ceci :
![Alt text](image/img_readme.png)
3. Lancez le fichier `start.bat`.

#### Exécution avec paramètres spécifiques
Pour personnaliser les paramètres réseau ou désactiver la cinématique, utilisez la commande suivante dans un terminal :
```bash
.\start.bat device port cinematique
```
- `device` : Wi-Fi
- `cinematique` : True ou False pour lancer la cinématique vidéo au debut et à la fin de la partie.

### Jeu Multijoueur
1. Ouvrez un projet vide dans **Ingescape Circle V4**.
2. Connectez-vous au réseau Wi-Fi **5670**.

#### Pour l’hôte de la partie :
- Lancez le fichier `server.bat` pour démarrer le serveur.
- Ensuite, exécutez le fichier `start_multi.bat` pour lancer le jeu en mode multijoueur.

#### Pour les autres joueurs :
- Exécutez simplement le fichier `start_multi.bat` pour rejoindre la partie.

#### Exécution avec paramètres spécifiques
Pour modifier les paramètres réseau, utilisez la commande suivante dans un terminal :
```bash
.\start_multi.bat device port
 ```

## Commandes

### Commandes de Déplacement
- Avancer : `Z`
- Reculer : `S`
- Aller à Gauche : `Q`
- Aller à Droite : `D`
- Tourner à Gauche : `A`
- Tourner à Droite : `E`

### Commandes pour la Musique
- Couper les bruitages et la musique : `M`
- Couper uniquement la musique : `N`

### Commande de Debug
- Activer le mode debug : `P`

## Lien exemple gameplay

### Solo
https://youtu.be/SlaDNC0tvr0

### Multi
https://youtu.be/kgHKAu8CVC4

## Auteurs:

### Développeurs:
Baffogne Clara
Blayes Hugo

### Graphiste:
Piquer Alexia
