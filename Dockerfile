FROM python:3.7

RUN apt-get update && apt-get install -y python-all-dev portaudio19-dev
RUN python3.7 -m pip install pip --upgrade pip
