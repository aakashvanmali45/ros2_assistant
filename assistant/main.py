from assistant.assistant import handle_input

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = handle_input(user_input)
        print(response)
