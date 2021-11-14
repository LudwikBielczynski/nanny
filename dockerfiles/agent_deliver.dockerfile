FROM ubuntu:20.04

ARG USER_CONTAINER=deploy
RUN apt update && apt install openssh-server sudo -y

# COPY "/home/.ssh" "/root/.ssh"
COPY ssh_permissions /bin/ssh_permissions
RUN chmod +x /bin/ssh_permissions

# RUN useradd -rm -d /home/${USER_CONTAINER} -s /bin/bash -g root -G sudo -u 1000 ${USER_CONTAINER}
# RUN echo ${USER_CONTAINER}:${USER_CONTAINER} | chpasswd
# USER ${USER_CONTAINER}

ENTRYPOINT ["/bin/ssh_permissions"]
