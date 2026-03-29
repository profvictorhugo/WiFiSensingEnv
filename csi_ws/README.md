# csi_ws

Workspace ROS 2 com um pacote simples de publisher/subscriber para teste de comunicação via tópicos.

## Pacote: `csi`

- **Distribuição ROS 2**: Humble
- **Linguagem**: Python (`rclpy`)
- **Dependências**: `std_msgs`

### Nodes

| Node | Entry point | Tipo | Tópico |
|------|-------------|------|--------|
| `csi_publisher` | `csi.publisher_contador:main` | Publisher | `/contagem` (Int64) |
| `csi_subscriber` | `csi.subscriber_contador:main` | Subscriber | `/contagem` (Int64) |

- O publisher publica um contador incrementado a cada 1 segundo.
- O subscriber recebe os valores, conta as mensagens recebidas e loga um aviso a cada múltiplo de 5.

---

## Rodando localmente

```bash
cd csi_ws
colcon build --symlink-install
source install/setup.bash

# Terminal 1
ros2 run csi csi_publisher

# Terminal 2
ros2 run csi csi_subscriber
```

## Rodando com Docker

```bash
cd csi_ws
docker build -t csi:latest .

# Terminal 1
docker run --rm --network host csi:latest csi_publisher

# Terminal 2
docker run --rm --network host csi:latest csi_subscriber
```
