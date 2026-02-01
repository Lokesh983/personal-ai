import sys
import json

from brain import run_brain  # Project 6 entry point


def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "INVALID_INPUT",
            "details": "Expected exactly one argument containing JSON input"
        }))
        sys.exit(1)

    raw_input = sys.argv[1]

    try:
        normalized_input = json.loads(raw_input)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": "INVALID_JSON",
            "details": str(e)
        }))
        sys.exit(1)

    result = run_brain(normalized_input)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
