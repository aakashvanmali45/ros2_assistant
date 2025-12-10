import subprocess
import json
import os
import sys

from dotenv import load_dotenv

from code_writer import (
    add_client_to_node,
    add_publisher_to_node,
    add_service_to_node,
    add_subscriber_to_node,
    add_timer_to_node,
)
from interpretor import interpret_text

load_dotenv()

def retrieve_context():
    subprocess.run(
        [sys.executable, "assistant/read_context_v2.py"],
        check=True,
        capture_output=True,
        text=True,
    )


def parse_json_command(command):
    parsed = json.loads(command)

    filepath = f"src/test_pkg/test_pkg/{parsed['filename']}"

    match parsed["action"]:
        case "add_publisher":
            add_publisher_to_node(filepath, parsed["topic"], parsed["msg_type"])
        case "add_subscriber":
            add_subscriber_to_node(filepath, parsed["topic"], parsed["msg_type"])
        case "add_service":
            add_service_to_node(
                filepath, parsed["service_name"], parsed["service_type"]
            )
        case "add_client":
            add_client_to_node(
                filepath, parsed["service_name"], parsed["service_type"]
            )
        case "add_timer":
            add_timer_to_node(filepath, float(parsed["period"]))
        case _:
            print("🚫 Unsupported action")


def main():
    user_input = input("Enter Command: ")
    json_command = interpret_text(user_input)
    print(json_command)
    parse_json_command(json_command)
    retrieve_context()


if __name__ == "__main__":
    main()
