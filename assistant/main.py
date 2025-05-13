from assistant.assistant import handle_input

if __name__ == "__main__":
    print("ROS 2 LLM Assistant. Type 'exit' to quit.")
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        try:
            response = handle_input(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
