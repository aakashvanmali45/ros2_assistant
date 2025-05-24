import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from std_msgs.msg import String
from std_msgs.msg import Int64

class Test_nodeNode(Node):
    def __init__(self):
        super().__init__('test_node')
        self.timer_1_ = self.create_timer(3.0, self.timer_callback)
        self.timer_ = self.create_timer(2.0, self.timer_callback)
        self.publisher_ = self.create_publisher(Int64, "/number", 10)
        #self.publisher_ = self.create_publisher(String, "/sensor_data", 10)
        
        #self.get_logger().info('test_node node has been started')
        #self.publisher_ = self.create_publisher(Int64, "test", 10)

def main(args=None):
    rclpy.init(args=args)
    node = Test_nodeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
            
        