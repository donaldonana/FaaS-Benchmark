## Thumbnaille

Le benchmark télécharge une image depuis le stockage distant, puis la passe en paramétre à une fonction qui la redimensionne à la taille d'une vignette. Upload ensuite la nouvelle version plus petite de l’image. Pour les expérimentations, nous avons sélectionné des images de tailles différentes  provenant du jeu de données image-net.

## How ro run ? 
Nous avons écrit un script bash pour exécuter automatiquement les expérimentation pour ce benchmark. Il s'exécute commme suit: 

./run.sh ipv4 run update image 

**ipv4**: l'afresse ipv4 de la machine haute 

**update**: un bolean. if the value is "1" the action was update, or create if does not exist

**run**: un boleann. if the value is "1", the experiment will start, then the action will be invoke n consecutif time. 

**image**: the name of the image file to resize. 

*example*: ./run.sh 123.13.34.201 1 1 image.png

## Some results ? 

 