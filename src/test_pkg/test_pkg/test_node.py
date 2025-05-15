import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class Test_nodeNode(Node):
    def __init__(self):
        super().__init__('test_node')
        self.get_logger().info('test_node node has been started')
        self.publisher_ = self.create_publisher(Int64, "test", 10)

def main(args=None):
    rclpy.init(args=args)
    node = Test_nodeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
            