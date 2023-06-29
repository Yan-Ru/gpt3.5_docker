FROM python:3.9

# 设置非特权用户及其UID和GID
ARG USER_NAME=harrison
ARG USER_ID=1000
ARG GROUP_ID=1000
ENV USER=harrison
ENV OPENAI_API_KEY=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

RUN apt-get update && apt-get install -y \
    curl \
    nano \
    x11-apps \
    mesa-utils \
    sudo

# 创建一个非特权用户并设置用户ID和组ID
RUN groupadd --gid ${GROUP_ID} ${USER_NAME} && \
    useradd --uid ${USER_ID} --gid ${GROUP_ID} --create-home ${USER_NAME} && \
    # 将用户添加到sudoers文件中（如果需要）
    usermod -aG sudo ${USER_NAME} && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN pip install openai

# 切换到非特权用户
USER ${USER_NAME}

#COPY output.json /home/${USER_NAME}/app/
#COPY gpt_call.py /home/${USER_NAME}/app/ 

WORKDIR /home/${USER_NAME}/app
#RUN /bin/bash -c "sudo chmod 777 output.json"

#VOLUME ["/home/${USER_NAME}/app"]

ENTRYPOINT python gpt_call.py
#ENTRYPOINT [ "bash" ]
