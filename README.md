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
2. Connectez-vous au réseau Wi-Fi **5670**. Le cadran doit se colorer en orange.
3. Lancez le fichier `start.bat`.

#### Exécution avec paramètres spécifiques
Pour personnaliser les paramètres réseau ou désactiver la cinématique, utilisez la commande suivante dans un terminal :
```bash
.\start.bat device port cinematique
```
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