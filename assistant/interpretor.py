import openai

#openai.api_key=""

def interpret_text(user_input):
    prompt = f"""
You are a code assistant for ROS2.

Your job is to take user instructions and convert them to structured JSON commands like this:

Input: "add a publisher to topic /sensor_data with msg type std_msgs.msg.String in test_node.py"
Output:
{{
  "action": "add_publisher",
  "filename": "test_node.py",
  "topic": "/sensor_data",
  "msg_type": "std_msgs.msg.String"
}}

Only return the JSON object. Here is the input:
{user_input}
"""
    response = openai.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content