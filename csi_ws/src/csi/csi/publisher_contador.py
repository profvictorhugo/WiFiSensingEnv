import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class CsiPublisher(Node):

    def __init__(self):
        super().__init__('csi_publisher')
        self.publisher_ = self.create_publisher(Int64, 'contagem', 10)
        self.contador = 0
        self.timer = self.create_timer(1.0, self.publicar)
        self.get_logger().info('Publicando em /contagem...')

    def publicar(self):
        msg = Int64()
        msg.data = self.contador

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicado: {msg.data}')
        self.contador += 1


def main(args=None):
    rclpy.init(args=args)
    no = CsiPublisher()

    rclpy.spin(no)

    no.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
