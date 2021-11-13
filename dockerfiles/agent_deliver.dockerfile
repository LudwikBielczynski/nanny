FROM ubuntu:20.04

ARG USER_CONTAINER=deploy
RUN apt update && apt install openssh-server sudo -y
RUN useradd -rm -s /bin/bash -g root -G sudo -u 1000 ${USER_CONTAINER}
RUN echo ${USER_CONTAINER}:${USER_CONTAINER} | chpasswd

COPY ssh_permissions /bin/ssh_permissions
RUN chmod +x /bin/ssh_permissions

USER ${USER_CONTAINER}
ENTRYPOINT ["/bin/ssh_permissions"]
