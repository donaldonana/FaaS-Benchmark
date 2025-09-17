
We implement state-of-the-art FaaS benchmark and differents alternatives. Deploying and executing them on Apache OpenWhisk. During execution, we monitor energy consumption, execution time, and result quality for each alternative. We have provided more details in the file `rapport.pdf`  

## Requirements : 

  * Install and configure Apache OpenWhisk
  
  * Install and configure Swift OpenStack 
  

## Folders Description : 

More description of each benchmark, are avaible in `rapport.pdf`  file. 

  * `thumbnaile`:  The folder contain the thumbnaile bench implementation. the benchmark downloads an image from cloud storage (swift in our case), resizes it to a thumbnail size, and then uploads the new smaller version of the image.
  
  * `image-recognition`: The folder contain image-recognition benchmark implementation. The benchmark performs an image recognition task. It starts by downloading an image from cloud storage, then submits it as input to a ResNet model, a deep learning model specifically designed for image recognition. 
  
  * `video-processing`: The folder contain  video-processing benchmark implementation. This benchmark downloads a video from remote storage, transforms it into an image in GIF format, and then returns the result.
  
  * `text-to-speech`: The folder contain the text-to-speech benchmark implementation. The benchmark implements an application that converts a text file into audio. It takes a text as input and produces an audio file as output, encoded in a specific format. It is the multi step benchmark so the folder have others sub-folder for each step implementation. 

  * `Facial-recognition`: The folder contain the Facial-recognition benchmark implementation. The benchmark implements a facial recognition application, it takes as input an image containing the face of an actor and a video, then draws a bounding box around the actor’s face in all the scenes of the video. As text-to-speech bench, it is a multi step benchmark.  

  
 