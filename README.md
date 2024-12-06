## GreenFaaS

L'objectif  est de proposer une architecture des services FaaS permettant d’exécuter les fonctions  en consommant le moins d’énergie possible, tout en maintenant au mieux la qualité du résultat attendue par l'utilisateur. Pour cela nous proposons GreenFaaS une solution dans laquelle, pour une fonction    destinée à réaliser une tâche, le client pourra enregistrer plusieurs implémentations alternatives. Les alternatives  seront différentes les unes des autres soit par l'algorithme utilisé, soit par les ressources allouées pour l'exécution. Le fournisseur de service, en  fonction de  son budget énergétique et en tenant compte des attentes de l’utilisateur,  déterminera et proposera l’alternative  qui consomme moins d’énergie  et  qui produit un résultat de qualité acceptable par l’utilisateur. 

Dans l’optique de consolider l’idée proposée, le stagiaire devra tout d’abord produire la partie motivation du projet, c'est-à-dire proposer des implémentations alternatives d’un ensemble de benchmark de l'état de l’art. Ensuite implémenter et exécuter ces alternatives sur apache openwhisk (une plate-forme open source conçue pour développer et déployer des fonctions sur le cloud), en  monitorant la consommation énergétique, le temps d’exécution, et la qualité du résultat produit par chaque alternative. 

## How to Run ? 

1. Install openwhisk
2. Install OpenstackSwift
