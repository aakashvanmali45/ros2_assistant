import subprocess
import json
from interpretor import interpret_text
from code_writer import add_publisher_to_node
from openai import OpenAI

import os

from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")


def retrieve_context():
    subprocess.run(["python3", "assistant/read_context_v2.py"])
    

def parse_json_command(command):
    pass

def main():
    print(f"API Key Loaded: {api_key}...")
    retrieve_context()

    user_input = input("Enter Command: ")
    json_command = interpret_text(user_input)
    print(json_command)
      # Only partial key for safety





if __name__ == "__main__":
    main()