FROM ubuntu:20.04

RUN apt update && apt install openssh-server sudo -y

# COPY /tmp/.ssh /root/.ssh
# RUN chmod 700 /root/.ssh
# RUN chmod 644 /root/.ssh/id_rsa.pub
# RUN chmod 600 /root/.ssh/id_rsa
