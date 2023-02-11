FROM alpine/git

WORKDIR /root
COPY ctf-base .
COPY motd /etc/motd

RUN mkdir -p /root/.ssh \
    && chmod 0700 /root/.ssh \
    && echo 'root:somepassword' | chpasswd \
    && apk add openrc openssh \
    && echo -e "PermitRootLogin yes" >> /etc/ssh/sshd_config \
    && mkdir -p /run/openrc \
    && touch /run/openrc/softlevel

COPY ssh/id_rsa /root/.ssh/id_rsa
COPY ssh/id_rsa.pub /root/.ssh/id_rsa.pub


ENTRYPOINT [ "sh", "-c", "rc-status; rc-service sshd start; while true; do sleep 1; done" ]