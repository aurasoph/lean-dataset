from lean_interact import LeanREPLConfig, TempRequireProject, LeanRequire, LeanServer, FileCommand, Command
from openai import OpenAI
import re


def generate_one_example(lines):
    return "example " + ''.join(['(' + i + ') ' for i in lines[:-1]]) + ':' + lines[-1][1:] + " := by"


def process_message(data):
    if data == "Goals accomplished!":
        return []
    assert data.split('\n', 1)[0] == "unsolved goals", "expected first line to be 'unsolved goals', was '" + data.split('\n', 1)[0] + "'"
    data = data.split('\n', 1)[1]
    
    return [generate_one_example(block.strip().split('\n')[1:] if block[:4] == "case" else block.strip().split('\n')) for block in data.split('\n\n')]


def generate_examples(interact_messages):
    return [goal for goals in (process_message(message.data) for message in interact_messages if not message.data.startswith("unexpected end of input;")) for goal in goals]


def get_info_view(interact_messages):
    return '\n\n'.join([goal for goals in (message.data for message in interact_messages) for goal in goals])

def get_ai_response(example):
    with open("OPEN_AI_API_KEY.txt", 'r') as f:
        api_key = f.read()
    client = OpenAI(api_key=api_key)

    print("Made OpenAI API call.")

    response = client.responses.create(
        model="gpt-4o",
        instructions="You receive an example statement or theorem in LEAN 4 and output the first line of the proof of the theorem. You produce only LEAN 4 code. You produce no natural language. You produce exactly one line of LEAN 4 code.",
        input=example
    )

    res_text = response.output_text

    if res_text.startswith("```lean\n"):
        res_text = res_text[8:]
    
    if res_text.endswith("```"):
        res_text = res_text[:-3]

    return res_text

def solve_example(statement):
    imports = "import Mathlib"
    config = LeanREPLConfig(
        lean_version="v4.19.0",
        project=TempRequireProject([
            LeanRequire(
                name="mathlib",
                git="https://github.com/leanprover-community/mathlib4.git",
                rev="v4.19.0"
            )
        ])
    )

    server = LeanServer(config)
    lines = statement + "\n"
    to_solve = [statement]
    print(statement)
    for i in range(50):
        response = get_ai_response(to_solve[0])
        print(response)
        lines += "  " * len(to_solve) + response + "\n"
        print(to_solve[0] + "\n  " + response)
        messages = server.run(Command(cmd=imports + "\n" + to_solve[0] + "\n  " + response)).messages
        to_solve = generate_examples(messages) + to_solve[1:]
        if len(to_solve) == 0:
            break
    return lines

        

if __name__ == "__main__":
    print(solve_example("""example (a b : ℝ) : a^3 - b^3 = (a-b)*(a^2+a*b+b^2) := by"""))

    
