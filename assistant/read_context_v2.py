import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Union

PACKAGE_NAME = "test_pkg"
SRC_PATH = Path.cwd() / "src" / PACKAGE_NAME / PACKAGE_NAME
CACHE_PATH = Path.cwd() / "assistant" / "context2.json"


def extract_ros_info(filepath: Path) -> Dict[str, Any]:
    """
    Extracts ROS-related information from a Python file's AST.

    Args:
        filepath: The path to the Python file.

    Returns:
        A dictionary containing extracted ROS information.
    """
    with open(filepath, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    node_info: Dict[str, Any] = {
        "filename": filepath.name,
        "filepath": str(filepath),  # Store as string for JSON serialization
        "class_name": None,
        "functions": [],
        "imports": [],
        "publishers": [],
        "subscribers": [],
        "clients": [],
        "services": [],
        "timers": [],
    }

    def get_safe_arg(
        node_args: List[ast.expr], index: int
    ) -> Union[str, int, float, bool, None]:
        """
        Safely extracts an argument from an AST Call node.
        Tries to evaluate it as a literal; falls back to unparsing if it fails.
        """
        if len(node_args) <= index:
            return "Unknown"
        try:
            # ast.literal_eval is safe for literals, but can fail on complex expressions
            return ast.literal_eval(node_args[index])
        except (ValueError, SyntaxError):
            # Fallback to unparsing the AST node if it's not a simple literal
            return ast.unparse(node_args[index])
        except Exception:  # Catch any other unexpected errors during literal_eval
            # This is a broad catch, but given the fallback is ast.unparse,
            # it's a reasonable last resort for unexpected AST node types.
            return ast.unparse(node_args[index])

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

            if func_name == "create_publisher":
                msg_type = get_safe_arg(node.args, 0)
                topic = get_safe_arg(node.args, 1)
                node_info["publishers"].append(
                    {
                        "topic": topic,
                        "msg_type": msg_type,
                    }
                )

            elif func_name == "create_subscription":
                msg_type = get_safe_arg(node.args, 0)
                topic = get_safe_arg(node.args, 1)
                node_info["subscribers"].append({"topic": topic, "msg_type": msg_type})

            elif func_name == "create_service":
                service_type = get_safe_arg(node.args, 0)
                service_name = get_safe_arg(node.args, 1)
                node_info["services"].append(
                    {"service_type": service_type, "service_name": service_name}
                )

            elif func_name == "create_client":
                client = get_safe_arg(node.args, 0)
                service_name = get_safe_arg(node.args, 1)
                node_info["clients"].append(
                    {"client": client, "service_name": service_name}
                )

            elif func_name == "create_timer":
                period = get_safe_arg(node.args, 0)
                node_info["timers"].append({"period": period})

    return node_info


def scan_package(path: Path) -> Dict[str, Any]:
    """
    Scans a directory for Python files and extracts ROS information.

    Args:
        path: The root path of the package to scan.

    Returns:
        A dictionary where keys are relative file paths and values are
        the extracted ROS information for each file.
    """
    results: Dict[str, Any] = {}
    for full_path in path.rglob("*.py"):  # Use rglob for recursive search
        node_result = extract_ros_info(full_path)
        rel_path = str(full_path.relative_to(path))  # Convert to string for dictionary key
        results[rel_path] = node_result
    return results


def save_json(context: Dict[str, Any]) -> None:
    """
    Saves the extracted context to a JSON file.

    Args:
        context: The dictionary containing the extracted ROS context.
    """
    # Ensure the cache directory exists
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(context, f, indent=2)


if __name__ == "__main__":
    context = scan_package(SRC_PATH)
    save_json(context)
    print(f"✅ Context extracted and saved to: {CACHE_PATH}")
