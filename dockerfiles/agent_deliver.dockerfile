FROM ubuntu:20.04

RUN apt update && apt install openssh-server sudo -y
RUN useradd -s /bin/bash -g root -G sudo -u 1000 test
RUN  echo 'test:test' | chpasswd

COPY ssh_permissions /bin/ssh_permissions
RUN chmod +x /bin/ssh_permissions
ENTRYPOINT ["/bin/ssh_permissions"]

