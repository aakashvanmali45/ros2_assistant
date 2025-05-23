# ROS2 Assistant Using LLMs

A smart and evolving assistant for ROS2 development using Large Language Models (LLMs). This tool interprets natural language commands and generates ROS2 Python code—nodes, publishers, subscribers, services, clients, and timers—automatically. 


---

## Features

The assistant can read raw human input and convert it into actionable commands which can be than parsed to write the code

- Generate ROS2 nodes from natural language commands.
- Add publishers, subscribers, services, clients, and timers automatically.
- Store node structures as JSON for future context-aware code insertion.


---

## Tech Stack

- **Ubuntu 24.04.2 LTS**
- **ROS2 Jazzy**
- **OpenAI GPT-4 API**
- **Python 3**

---

## How to Use

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ros2-assistant.git
   cd ros2-assistant

2. **Install Dependencies**
   ```bash
   python3 assistant/agent.py

3. **Add Your Command**
   Add a publisher to the topic /numbers with std_msgs/msg/Int64.
   Add a timer that triggers every 2 seconds.

## Future Scope

- Integrate new node creation within existing packages.
- Handle edge cases (e.g., node doesn't exist → ask to create or locate).
- Auto-update setup.py and package.xml on new node/package creation.
- Add support for callback generation for publishers/services/timers.
- Enable creation of custom interfaces for services and messages.
- Fine-tune LLM on official ROS2 documentation for more accurate outputs.
- Integrate an LLM Agent that reviews and suggests code improvements.

## Contribute or Collaborate

This project is under active development. If you're working on something similar or want to contribute ideas, improvements, or code—feel free to reach out or open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

   
