## Thumbnaille

This benchmark downloads an image from cloud storage, resizes it to a thumbnail size, and then uploads the new smaller version of the image. For the experiments, we selected images of different sizes from the image-net dataset mainly used in scientific research for image processing. 

## How ro run ? 
We wrote a bash script to automatically run the experiments for this benchmark. It runs as follows:

./run.sh &lt;ipv4&gt; &lt;run&gt; &lt;update&gt; &lt;image&gt; 

**ipv4**: l'afresse ipv4 de la machine host 

**update**: un bolean. if the value is "1" the action will be update, or create if does not exist. 

**run**: un boleann. if the value is "1", the experiment will start, then the action will be invoke 100 consecutif time. 

**image**: the name of the image passed as a parameter. 

*example*: ./run.sh 123.13.34.202 1 1 image.png

## Some results ? 

 