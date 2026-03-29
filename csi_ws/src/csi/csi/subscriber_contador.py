import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class CsiSubscriber(Node):

    def __init__(self):
        super().__init__('csi_subscriber')

        self.subscription = self.create_subscription(
            Int64,
            'contagem',
            self.callback,
            10
        )
        self.total_recebido = 0
        self.get_logger().info('Ouvindo /contagem...')

    def callback(self, msg):
        self.total_recebido += 1
        self.get_logger().info(
            f'Recebi: {msg.data} | Total recebido: {self.total_recebido}'
        )

        if msg.data % 5 == 0 and msg.data != 0:
            self.get_logger().warn(f'Múltiplo de 5 detectado: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    no = CsiSubscriber()
    
    rclpy.spin(no)

    no.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
