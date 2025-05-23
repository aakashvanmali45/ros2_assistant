from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpret_text(user_input):
    prompt = f"""
You are a code assistant for ROS2.

Convert user input into structured JSON commands. Supported actions:

1. add_publisher
2. add_subscriber
3. add_service
4. add_client


Use this format:
{{
  "action": "add_publisher",
  "filename": "test_node.py",
  "topic_name": "/sensor_data",
  "message_type": "std_msgs.msg.String"
}}

1. add_timer
Use this format:
{{
  "action": "add_timer",
  "filename": "test_node.py",
  "period": "0.5",
  
}}

Only return JSON. Here’s the input:
{user_input}
"""

    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content