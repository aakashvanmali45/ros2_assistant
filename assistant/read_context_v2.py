import os 
import ast
import json

PACKAGE_NAME = "test_pkg"
SRC_PATH = os.path.join(os.getcwd(), "src",PACKAGE_NAME, PACKAGE_NAME)
CACHE_PATH = os.path.join(os.getcwd(), "assistant", "context.json")

def extract_ros_info(filepath):
    with open(filepath, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    node_info = {
        "filename": os.path.basename(filepath),
        "publisher":[],
        "subscriber": [],
        "clients": [],
        "services": [],
        "timers": [],
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            if func_name == "create_publisher":
                msg_type = ast.unparse(node.args[0]) if node.args else "Unknown"
                topic = node.args[1].value if len(node.args)>1 else "Unknown"
                node_info["publisher"].append({
                    "topic": topic,
                    "msg_type": msg_type,
    
                })

            elif func_name == "create_subscription":
                msg_type = ast.unparse(node.args[0]) if node.args else "Unknown"
                topic = node.args[1].value if len(node.args) > 1 else "Unknown"
                node_info["subscribers"].append({
                    "topic": topic,
                    "msg_type": msg_type
                })

            elif func_name == "create_service":
                service_type = ast.unparse(node.args[0]) if node.args else "Unknown"
                service_name = node.args[1].value if len(node.args)>1 else "Unknown"
                node_info["services"].append({
                    "service_type": service_type,
                    "service_name": service_name
                })

            elif func_name == "create_client":
                client = ast.unparse(node.args[0]) if node.args else "Unknown"
                service_name = node.args[1].value if len(node.args)>1 else "Unknown"
                node_info["clients"].append({
                    "Client": client,
                    "service_name": service_name
                })

            elif func_name == "create_timer":
                period = ast.unparse(node.args[0]) if node.args else "Unknown"
                node_info["timers"].append({
                    "period": period
                })
    return node_info

def scan_package(path):
    results = {}
    for file in os.listdir(path):
        if file.endswith(".py"):
            full_path = os.path.join(path, file)
            node_result = extract_ros_info(full_path)
            results[file] = node_result
    return results

def save_json(context):
    with open(CACHE_PATH, "w") as f:
        json.dump(context, f, indent=2)



if __name__ == "__main__":
    context = scan_package(SRC_PATH)
    save_json(context)
    print(f"Context extracted to {CACHE_PATH}")