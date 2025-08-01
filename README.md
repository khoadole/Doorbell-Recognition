# Doorbell Recognition

**Doorbell Recognition** is a web application built with Django that allows users to stream video from a door camera and remotely control door access. Device run face detection on device and process face recognition on server.

## Python version: 3.11.13

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/khoadole/Doorbell-Recognition.git
cd doorbell-recognition
```

2. **Dowload [vggface model](https://drive.google.com/drive/folders/1R61CxS43kbhpZla1BA2RXlc6a1OGMKtO?usp=sharing) and put it next to _manage.py_ file** 

3. When downloading library from **requirement.txt** if you got error on **tensorflow-io-gcs-filesystem==0.37.1**, then delete the line from file and download **tensorflow==2.18.0** alone first.

4. You can get device code from this [link](https://drive.google.com/drive/folders/1CxTw8mEpGqvmDdCB50iSLD6W3MsFwykR?usp=sharing)

## For device's model test image
Create a folder name **saved_image** next to _manage.py_ file
