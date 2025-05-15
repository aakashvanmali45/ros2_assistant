import os
import re

PACKAGE_NAME = "test_pkg"
SRC_PATH = os.path.join(os.getcwd(), "src",PACKAGE_NAME, PACKAGE_NAME)
example_command= "Follow the sample command: make a node named sample_node"
print(example_command)
user_input = input("Enter Command: ")

match = re.search(r"make a node named (\w+)", user_input.lower())

if match:
    node_name = match.group(1)
    node_filename = f"{node_name}.py"
    node_path = os.path.join(SRC_PATH, node_filename)

    if not os.path.exists(node_path):
        with open(node_path, "w") as f:
            f.write(
                f"""import rclpy
from rclpy.node import Node

class {node_name.capitalize()}Node(Node):
    def __init__(self):
        super().__init__('{node_name}')
        self.get_logger().info('{node_name} node has been started')

def main(args=None):
    rclpy.init(args=args)
    node = {node_name.capitalize()}Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
            """)
            print(f"Node {node_name}.py created at {node_path}")

    else:
        print(f"Node {node_name}.py already exists")

else:
    print("Could not parse node")

