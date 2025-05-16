import os
import ast
import json

PACKAGE_NAME = "test_pkg"
SRC_PATH = os.path.join(os.getcwd(), "src", PACKAGE_NAME, PACKAGE_NAME)
CACHE_PATH = os.path.join(os.getcwd(), "assistant", "context2.json")


def extract_ros_info(filepath):
    with open(filepath, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    node_info = {
        "filename": os.path.basename(filepath),
        "filepath": filepath,
        "class_name": None,
        "functions": [],
        "imports": [],
        "publishers": [],
        "subscribers": [],
        "clients": [],
        "services": [],
        "timers": [],
    }

    for node in ast.walk(tree):
        # Imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            node_info["imports"].append(ast.unparse(node))

        # Class name
        elif isinstance(node, ast.ClassDef):
            node_info["class_name"] = node.name

        # Functions
        elif isinstance(node, ast.FunctionDef):
            node_info["functions"].append(node.name)

        # ROS functionality
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

            def get_safe_arg(index):
                try:
                    return ast.literal_eval(node.args[index])
                except:
                    return ast.unparse(node.args[index]) if len(node.args) > index else "Unknown"

            if func_name == "create_publisher":
                msg_type = get_safe_arg(0)
                topic = get_safe_arg(1)
                node_info["publishers"].append({
                    "topic": topic,
                    "msg_type": msg_type,
                })

            elif func_name == "create_subscription":
                msg_type = get_safe_arg(0)
                topic = get_safe_arg(1)
                node_info["subscribers"].append({
                    "topic": topic,
                    "msg_type": msg_type
                })

            elif func_name == "create_service":
                service_type = get_safe_arg(0)
                service_name = get_safe_arg(1)
                node_info["services"].append({
                    "service_type": service_type,
                    "service_name": service_name
                })

            elif func_name == "create_client":
                client = get_safe_arg(0)
                service_name = get_safe_arg(1)
                node_info["clients"].append({
                    "client": client,
                    "service_name": service_name
                })

            elif func_name == "create_timer":
                period = get_safe_arg(0)
                node_info["timers"].append({
                    "period": period
                })

    return node_info


def scan_package(path):
    results = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                node_result = extract_ros_info(full_path)
                rel_path = os.path.relpath(full_path, path)
                results[rel_path] = node_result
    return results


def save_json(context):
    with open(CACHE_PATH, "w") as f:
        json.dump(context, f, indent=2)


if __name__ == "__main__":
    context = scan_package(SRC_PATH)
    save_json(context)
    print(f"✅ Context extracted and saved to: {CACHE_PATH}")
