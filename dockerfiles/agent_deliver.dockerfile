FROM ubuntu:20.04

RUN apt update && apt install openssh-server sudo -y

COPY ssh_permissions /bin/ssh_permissions
RUN chmod +x /bin/ssh_permissions
ENTRYPOINT ["/bin/ssh_permissions"]
