import json
import ast
import os

CONTEXT_PATH = "assistant/context.json"
SRC_ROOT = os.path.join(os.getcwd(), "src", "test_pkg", "test_pkg")

def generate_unique_variable_name(lines, base_name):
    count = 1
    while True:
        candidate = f"{base_name}_{count}"
        if not any(candidate in lines for line in lines):
            return candidate
        count+=1

def load_context():
    with open(CONTEXT_PATH, "r") as f:
        return json.load(f)


def ensure_import_exists(code, import_stmt):
    return import_stmt not in code


def add_publisher_to_node(filepath, topic_name, message_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    # Check for import and add if missing
    import_stmt = f"from {message_type.rsplit('.', 1)[0]} import {message_type.rsplit('.', 1)[-1]}" #
    if ensure_import_exists("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                continue
            lines.insert(i, import_stmt + "\n")
            break

    var_name = generate_unique_variable_name(lines, "publisher")


    # Inject into __init__
    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            publisher_line = f'{indent}self.{var_name}_ = self.create_publisher({message_type.rsplit('.', 1)[-1]}, "{topic_name}", 10)\n'
            if publisher_line.strip() not in "".join(lines):
                lines.insert(i + 2, publisher_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Publisher added to {filepath}")

def add_subscriber_to_node(filepath, topic, msg_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    import_stmt = f"from {msg_type.rsplit('.', 1)[0]} import {msg_type.rsplit('.', 1)[-1]}" #
    if ensure_import_exists("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                continue
            lines.insert(i, import_stmt + "\n")
            break

    var_name = generate_unique_variable_name(lines, "subscriber")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            subscriber_line = f'{indent}self.{var_name} = self.create_subscription({msg_type.rsplit('.', 1)[-1]}, "{topic}", 10)\n'
            if subscriber_line.strip() not in "".join(lines):
                add_line = "        # Add 'def listener_callback(self, msg): pass'\n"
                lines.insert(i + 2, subscriber_line)
                lines.insert(add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Subscriber added to {filepath}")
    

def add_service_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    import_stmt = f"from {service_type.rsplit('.', 1)[0]} import {service_type.rsplit('.', 1)[-1]}" #
    if ensure_import_exists("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                continue
            lines.insert(i, import_stmt + "\n")
            break

    var_name = generate_unique_variable_name(lines, "service")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            service_line = f'{indent}self.{var_name} = self.create_service({service_type}, "{service_name}",  self.handle_service)\n'
            if service_line.strip() not in "".join(lines):
                add_line = "        # Add 'def handle_service(self, request, response): pass'\n"
                lines.insert(i + 2, service_line)
                lines.insert(add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Service added to {filepath}")
    
    
def add_client_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    import_stmt = f"from {service_type.rsplit('.', 1)[0]} import {service_type.rsplit('.', 1)[-1]}" #
    if ensure_import_exists("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                continue
            lines.insert(i, import_stmt + "\n")
            break

    var_name = generate_unique_variable_name(lines, "client")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            client_line = f'{indent}self.{var_name} = self.create_service({service_type.rsplit('.', 1)[-1]}, "{service_name}")\n'
            if client_line.strip() not in "".join(lines):
                
                lines.insert(i + 2, client_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Client added to {filepath}")
    
    
def add_timer_to_node(filepath, period=0.5):
    with open(filepath, "r") as f:
        lines = f.readlines()

    var_name = generate_unique_variable_name(lines, "timer")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            service_line = f'{indent}self.{var_name}_ = self.create_timer({period}, self.timer_callback)\n'
            if service_line.strip() not in "".join(lines):
                
                lines.insert(i + 2, service_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Timer added to {filepath}")
    


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