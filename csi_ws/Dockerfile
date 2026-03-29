FROM ros:humble

# instala dependências de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws
COPY src/ src/

# faz o build do workspace
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install

# entrypoint que sourca ROS e o workspace antes de qualquer CMD
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
