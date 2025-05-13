import os
import subprocess
import json

WS_SRC = os.path.expanduser("~/ros2_assistant_ws/src")

def create_package(pkg_name):
    cmd = f"ros2 pkg create --build-type ament_python {pkg_name}"
    subprocess.run(cmd, shell=True, cwd=WS_SRC)
    return f"Package '{pkg_name}' created."

def create_node(input_dict):
    try:
        if isinstance(input_dict, str):
            input_dict = json.loads(input_dict)

        pkg_name = input_dict.get("pkg_name")
        node_name = input_dict.get("node_name")

        if not pkg_name or not node_name:
            return "Missing 'pkg_name' or 'node_name'."

        pkg_path = os.path.join(WS_SRC, pkg_name, pkg_name)
        os.makedirs(pkg_path, exist_ok=True)
        file_path = os.path.join(pkg_path, f"{node_name}.py")

        content = f'''
import rclpy
from rclpy.node import Node

class {node_name.capitalize()}(Node):
    def __init__(self):
        super().__init__('{node_name}')
        self.get_logger().info("Node '{node_name}' has started!")

def main(args=None):
    rclpy.init(args=args)
    node = {node_name.capitalize()}()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
'''

        with open(file_path, 'w') as f:
            f.write(content)

        return f"Node '{node_name}.py' created in package '{pkg_name}'."

    except Exception as e:
        return str(e)
