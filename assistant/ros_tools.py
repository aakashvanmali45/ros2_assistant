import os
import subprocess

WS_SRC = os.path.expanduser("~/ros2_assistant_ws/src")

def create_package(pkg_name):
    cmd = f"ros2 pkg create --build-type ament_python {pkg_name}"
    subprocess.run(cmd, shell=True, cwd=WS_SRC)
    return f"Package {pkg_name} created."

def create_node(pkg_name, node_name):
    file_path = os.path.join(WS_SRC, pkg_name, pkg_name, f"{node_name}.py")
    content = f'''
import rclpy
from rclpy.node import Node

class {node_name.capitalize()}(Node):
    def __init__(self):
        super().__init__('{node_name}')
        self.get_logger().info("Node started!")

def main(args=None):
    rclpy.init(args=args)
    node = {node_name.capitalize()}()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
'''
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Node {node_name}.py created in package {pkg_name}."
