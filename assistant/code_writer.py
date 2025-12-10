import json
import os

CONTEXT_PATH = "assistant/context.json"
SRC_ROOT = os.path.join(os.getcwd(), "src", "test_pkg", "test_pkg")

def generate_unique_variable_name(lines, base_name):
    count = 1
    while True:
        candidate = f"{base_name}_{count}"
        # This check is broad and might match substrings. A more robust solution
        # would involve AST parsing to identify actual variable definitions.
        if not any(candidate in line for line in lines):
            return candidate
        count += 1

def load_context():
    with open(CONTEXT_PATH, "r") as f:
        return json.load(f)

def is_import_missing(code, import_stmt):
    """
    Checks if an import statement is missing from the code.
    Returns True if the import statement is NOT found in the code.
    """
    return import_stmt not in code

def _get_import_insertion_index(lines):
    """
    Determines the best line index to insert a new import statement.
    It tries to insert after the last existing import, or at the first
    non-empty, non-comment line if no imports exist.
    """
    last_import_idx = -1
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith("import ") or stripped_line.startswith("from "):
            last_import_idx = i
        elif stripped_line and not stripped_line.startswith("#"):
            # Found first non-import, non-comment, non-empty line
            if last_import_idx != -1:
                return last_import_idx + 1
            else:
                # No imports found, insert at the very beginning of code
                return i
    return len(lines)  # If file is empty or only comments/imports, append at end

def add_publisher_to_node(filepath, topic_name, message_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    module_path, class_name = message_type.rsplit('.', 1)
    import_stmt = f"from {module_path} import {class_name}"

    if is_import_missing("".join(lines), import_stmt):
        insert_idx = _get_import_insertion_index(lines)
        lines.insert(insert_idx, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "publisher")

    # Inject into __init__
    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            publisher_line = f'{indent}self.{var_name}_ = self.create_publisher({class_name}, "{topic_name}", 10)\n'
            if publisher_line.strip() not in "".join(lines):
                lines.insert(i + 2, publisher_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Publisher added to {filepath}")

def add_subscriber_to_node(filepath, topic, msg_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    module_path, class_name = msg_type.rsplit('.', 1)
    import_stmt = f"from {module_path} import {class_name}"

    if is_import_missing("".join(lines), import_stmt):
        insert_idx = _get_import_insertion_index(lines)
        lines.insert(insert_idx, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "subscriber")
    callback_func_name = f"{var_name}_callback"

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            # Bug fix: Added callback function to create_subscription
            subscriber_line = f'{indent}self.{var_name} = self.create_subscription({class_name}, "{topic}", self.{callback_func_name}, 10)\n'
            if subscriber_line.strip() not in "".join(lines):
                lines.insert(i + 2, subscriber_line)
                # Bug fix: insert the comment line correctly
                add_line = f'{indent}# Add \'def {callback_func_name}(self, msg): pass\'\n'
                lines.insert(i + 3, add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Subscriber added to {filepath}")

def add_service_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    module_path, class_name = service_type.rsplit('.', 1)
    import_stmt = f"from {module_path} import {class_name}"

    if is_import_missing("".join(lines), import_stmt):
        insert_idx = _get_import_insertion_index(lines)
        lines.insert(insert_idx, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "service")
    handler_func_name = f"handle_{var_name}"

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            # Bug fix: Use class_name for service type, and handler_func_name
            service_line = f'{indent}self.{var_name} = self.create_service({class_name}, "{service_name}", self.{handler_func_name})\n'
            if service_line.strip() not in "".join(lines):
                lines.insert(i + 2, service_line)
                # Bug fix: insert the comment line correctly
                add_line = f'{indent}# Add \'def {handler_func_name}(self, request, response): pass\'\n'
                lines.insert(i + 3, add_line)
            break

    with open(filepath, "w") as f:
        f.writelines(lines)
    print(f"✅ Service added to {filepath}")

def add_client_to_node(filepath, service_name, service_type):
    with open(filepath, "r") as f:
        lines = f.readlines()

    module_path, class_name = service_type.rsplit('.', 1)
    import_stmt = f"from {module_path} import {class_name}"

    if is_import_missing("".join(lines), import_stmt):
        insert_idx = _get_import_insertion_index(lines)
        lines.insert(insert_idx, import_stmt + "\n")

    var_name = generate_unique_variable_name(lines, "client")

    for i, line in enumerate(lines):
        if "def __init__(" in line and "self" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            # Bug fix: Use create_client instead of create_service
            client_line = f'{indent}self.{var_name} = self.create_client({class_name}, "{service_name}")\n'
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
            # Bug fix: Use the correct callback_func_name
            timer_line = f'{indent}self.{var_name}_ = self.create_timer({period}, self.{callback_func_name})\n'
            if timer_line.strip() not in "".join(lines):
                lines.insert(i + 2, timer_line)
                # Add a comment for the timer callback
                add_line = f'{indent}# Add \'def {callback_func_name}(self): pass\'\n'
                lines.insert(i + 3, add_line)
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

    # Potential security vulnerability: If instruction["filename"] comes from untrusted
    # user input, it could lead to path traversal. Consider using os.path.normpath
    # or pathlib.Path.resolve() to sanitize the path.
    target_file = os.path.join(SRC_ROOT, instruction["filename"])
    add_publisher_to_node(
        filepath=target_file,
        topic_name=instruction["topic"],
        message_type=instruction["msg_type"]
    )


if __name__ == "__main__":
    main()
