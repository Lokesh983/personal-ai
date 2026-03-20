from brain.src.brain import PersonalAIBrain


def main() -> None:
    brain = PersonalAIBrain()

    while True:
        try:
            user_input = input(">> ")
        except (EOFError, KeyboardInterrupt):
            break
        response = brain.process_request(user_input)
        print(response)


if __name__ == "__main__":
    main()
