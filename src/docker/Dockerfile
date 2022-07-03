#
# contents curator
#

FROM ubuntu

RUN export LANG=en_us.UTF-8

# install
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3 net-tools iputils-ping ufw
RUN apt install -y openssh-server
RUN apt install -y vim figlet tree tmux
RUN apt install -y pip

#
# install py package
#
RUN pip3 install python-daemon httpserver
RUN pip3 install watchdog

#
# env
#
ENV CC_PROMPT="\[\e[1;92m\]\u\[\e[m\]@\[\e[33m\]\h\[\e[m\]:\[\033[1;94m\]\w\[\e[m\]$ "
RUN echo 'PS1=$CC_PROMPT' >> ~/.bashrc
RUN mkdir -p /root/contents-curator

#
# copy src
#
COPY copy/* /root/.

#
# startup
#
ENTRYPOINT cd ~ && \
           [ -f "./contents-curator/TestBot.sh" ] && \
               cd contents-curator/ && ./TestBot.sh native || \
               ./TestBot.sh native

