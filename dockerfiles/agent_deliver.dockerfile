FROM ubuntu:20.04

ARG USER=deploy
RUN apt update && apt install openssh-server sudo -y
RUN useradd -s /bin/bash -g root -G sudo -u 1000 ${USER}
RUN echo '${USER}:${USER}' | chpasswd

COPY ssh_permissions /bin/ssh_permissions
RUN chmod +x /bin/ssh_permissions

USER ${USER}
ENTRYPOINT ["/bin/ssh_permissions"]
