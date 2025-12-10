import json
import os

CONTEXT_PATH = "assistant/context.json"
SRC_ROOT = os.path.join(os.getcwd(), "src", "test_pkg", "test_pkg")

def generate_unique_variable_name(lines, base_name):
    count = 1
    while True:
        candidate = f"{base_name}_{count}"
        if not any(candidate in line for line in lines):
            return candidate
        count += 1

def load_context():
    with open(CONTEXT_PATH, "r") as f:
        return json.load(f)


def is_import_missing(code, import_stmt):
    """Returns True if the import statement is NOT found in the code."""
    return import_stmt not in code


def add_publisher_to_node(filepath, topic_name, message_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    msg_module = message_type.rsplit('.', 1)[0]
    msg_class = message_type.rsplit('.', 1)[-1]
    import_stmt = f"from {msg_module} import {msg_class}"

    if is_import_missing("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if not (line.startswith("import") or line.startswith("from") or line.strip() == ""):
                lines.insert(i, import_stmt + "\n")
                break
        else:
            lines.insert(0, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "publisher")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            publisher_line = f'{indent}self.{var_name}_ = self.create_publisher({msg_class}, "{topic_name}", 10)\n'
            if publisher_line.strip() not in "".join(lines):
                lines.insert(i + 2, publisher_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Publisher added to {filepath}")

def add_subscriber_to_node(filepath, topic, msg_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    msg_module = msg_type.rsplit('.', 1)[0]
    msg_class = msg_type.rsplit('.', 1)[-1]
    import_stmt = f"from {msg_module} import {msg_class}"

    if is_import_missing("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if not (line.startswith("import") or line.startswith("from") or line.strip() == ""):
                lines.insert(i, import_stmt + "\n")
                break
        else:
            lines.insert(0, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "subscriber")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            subscriber_line = f'{indent}self.{var_name}_ = self.create_subscription({msg_class}, "{topic}", self.listener_callback, 10)\n'
            if subscriber_line.strip() not in "".join(lines):
                add_line = f'{indent}# TODO: Implement the callback method: def listener_callback(self, msg): pass\n'
                lines.insert(i + 2, subscriber_line)
                lines.insert(i + 3, add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Subscriber added to {filepath}")
    

def add_service_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    srv_module = service_type.rsplit('.', 1)[0]
    srv_class = service_type.rsplit('.', 1)[-1]
    import_stmt = f"from {srv_module} import {srv_class}"

    if is_import_missing("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if not (line.startswith("import") or line.startswith("from") or line.strip() == ""):
                lines.insert(i, import_stmt + "\n")
                break
        else:
            lines.insert(0, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "service")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            service_line = f'{indent}self.{var_name}_ = self.create_service({srv_class}, "{service_name}",  self.handle_service)\n'
            if service_line.strip() not in "".join(lines):
                add_line = f'{indent}# TODO: Implement the service callback method: def handle_service(self, request, response): pass\n'
                lines.insert(i + 2, service_line)
                lines.insert(i + 3, add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Service added to {filepath}")
    
    
def add_client_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    srv_module = service_type.rsplit('.', 1)[0]
    srv_class = service_type.rsplit('.', 1)[-1]
    import_stmt = f"from {srv_module} import {srv_class}"

    if is_import_missing("".join(lines), import_stmt):
        for i, line in enumerate(lines):
            if not (line.startswith("import") or line.startswith("from") or line.strip() == ""):
                lines.insert(i, import_stmt + "\n")
                break
        else:
            lines.insert(0, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "client")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            client_line = f'{indent}self.{var_name}_ = self.create_client({srv_class}, "{service_name}")\n'
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
    callback_func_name = f"{var_name}_callback"

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            timer_line = f'{indent}self.{var_name}_ = self.create_timer({period}, self.{callback_func_name})\n'
            if timer_line.strip() not in "".join(lines):
                lines.insert(i + 2, timer_line)
                add_line = f'{indent}# TODO: Implement the timer callback method: def {callback_func_name}(self): pass\n'
                lines.insert(i + 3, add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Timer added to {filepath}")
    

def main():
    context = load_context()

    instruction = {
        "filename": "test_node.py",
        "msg_type": "std_msgs.msg.String",
        "topic": "/sensor_data"
    }

    target_file = os.path.join(SRC_ROOT, instruction["filename"])
    add_publisher_to_node(
        filepath=target_file,
        topic_name=instruction["topic"],
        message_type=instruction["msg_type"]
    )


if __name__ == "__main__":
    main()
