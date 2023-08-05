# MDtoHTML
Ce projet est sous license publique MIT.

## Comment ca marche ?

C'est très simple, il suffit d'installer le programme et ses addons.

Pour installer les addons, il faut ouvrir un terminal de commande et écrire :

Veillez à modifier FOLDER_PATH par le chemin d'accès du dossier ou vous avez installé le MDtoHTML.

```
cd FOLDER_PATH
pip install -r requirements.txt
```

Pour lancer le convertisseur il suffit de créer un (ou plusieurs fichiers) au format **.MD** dans un dossier quelconque et de lancer le programme dans un terminal.

```
python converter.py
```

Il suffit d'y ajouter des arguments, accessibles via --help à la suite de la commande ci dessus.

* Voici la liste des arguments ici :

  * --dir **OU** --input_directory ( Permet à l'utilisateur de convertir tous les fichiers MD d'un dossier avec une seule commande )


  * --i ( Si l'utilisateur veut préciser un fichier à convertir en particulier )


  * --o **OU** --output_directory ( La commande permettant de choisir la destination du fichier HTML sortant )


  * --title ( Commande permettant de changer le titre de ses page HTML converties )

## Librairie communautaire

Vous pouvez retrouver le package en tapant cette commande afin de l'utiliser dans d'autres projets :

```
pip install mdtohtmlfromju
```

Lien vers le package :


https://pypi.org/project/mdtohtmlfromju/


Si vous vous retrouvez avec ceci, c'est que le package est bien installé :

```
pip install mdtohtmlfromju
Collecting mdtohtmlfromju
  Downloading https://files.pythonhosted.org/packages/2e/88/908b916ea18fddeb6855a328b8d9d8618203d7b379c0267ec5910db717d9/mdtohtmlfromju-1.0.0-py3-none-any.whl
Installing collected packages: mdtohtmlfromju
Successfully installed mdtohtmlfromju-1.0.0
```