# scenesorter
split a sequence of images into a set of their changes

## Prerequisite

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

python -m pip install ––upgrade pip

python -m pip install imageio.v2
python -m pip install scipy.linalg
python -m pip install numpy
python -m pip install os
python -m pip install cv2
python -m pip install imutils 
``` 

## How to run
make sure you are in the directory that contains python script
put your folder that contains images in the same directory as  py script
make sure images are numbered

```
sudo docker build -t scenesorter .
docker run --rm -it -v ./media scenesorter
```
 