#!/bin/bash
<<<<<<< HEAD
#docker build --file Dockerfile --rm -t sro .
# rm -f singularity_images/*img
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /Users/henrymj/Documents/Self_Regulation_Ontology/singularity_images:/output --privileged -t singularityware/docker2singularity sro:matplotlib
# echo Finished Conversion
=======
docker build --file Dockerfile --rm -t sro .
rm -f singularity_images/*img
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /Users/henrymj/Documents/Self_Regulation_Ontology/singularity_images:/output --privileged -t singularityware/docker2singularity sro
echo Finished Conversion
>>>>>>> 7c37f9c012f5f17c869ea811d1bb7a1e0c45d033
cd singularity_images
# bash transfer_image.sh
# echo Finished Transfer
