import json
import ast
import os

CONTEXT_PATH = "assistant/context.json"
SRC_ROOT = os.path.join(os.getcwd(), "src", "test_pkg", "test_pkg")

def load_context():
    with open(CONTEXT_PATH, "r") as f:
        return json.load(f)


def ensure_import_exists(code, import_stmt):
    return import_stmt not in code


def add_publisher_to_node(filepath, topic, msg_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    # Check for import and add if missing
    import_stmt = f"from {msg_type.rsplit('.', 1)[0]} import {msg_type.rsplit('.', 1)[-1]}" #
    if ensure_import_exists("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                continue
            lines.insert(i, import_stmt + "\n")
            break

    # Inject into __init__
    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            publisher_line = f'{indent}self.publisher_ = self.create_publisher({msg_type.rsplit('.', 1)[-1]}, "{topic}", 10)\n'
            if publisher_line.strip() not in "".join(lines):
                lines.insert(i + 2, publisher_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Publisher added to {filepath}")


def main():
    context = load_context()

    # Example: Hardcoded for now — this will be replaced with agent input
    instruction = {
        "filename": "test_node.py",
        "msg_type": "std_msgs.msg.String",
        "topic": "/sensor_data"
    }

    target_file = os.path.join(SRC_ROOT, instruction["filename"])
    add_publisher_to_node(
        filepath=target_file,
        topic=instruction["topic"],
        msg_type=instruction["msg_type"]
    )


if __name__ == "__main__":
    main()
