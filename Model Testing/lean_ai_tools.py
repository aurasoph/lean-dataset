from lean_interact import LeanREPLConfig, TempRequireProject, LeanRequire, LeanServer, FileCommand, Command
from openai import OpenAI
import re, time

MINIF2F_INIT_STR = """import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat"""

LEAN_CONFIG = LeanREPLConfig(
    lean_version="v4.19.0",
    project=TempRequireProject([
        LeanRequire(
            name="mathlib",
            git="https://github.com/leanprover-community/mathlib4.git",
            rev="v4.19.0"
        )
    ])
)

class Chat:
    def __init__(self, system_prompt, model):
        with open("/Users/xvade/dev/LEAN/lean-dataset/lean-dataset/Model Testing/OPEN_AI_API_KEY.txt", 'r') as f:
            api_key = f.read()
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.messages = [{"role": "system", "content": system_prompt}]
        self.api_calls_made = 0
    
    def get_response(self, input):
        self.messages.append({"role": "user", "content": input})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        self.api_calls_made += 1
        self.messages.append(completion.choices[0].message)
        return completion.choices[0].message.content
        


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

def generate_reply(messages):
    return "There were some issues with that proof. You must change the following lines to resolve these issues\n\n" + "\n\n".join(["Line " + str(message.end_pos.line) + ": " + message.data for message in messages])

def clean_response(response):
    while "```lean" in response:
        response = response.split("```lean", 1)[1].strip()
    while "```" in response:
        response = response.split("```", 1)[0]
    return response


def get_ai_response(example):
    with open("/Users/xvade/dev/LEAN/lean-dataset/lean-dataset/Model Testing/OPEN_AI_API_KEY.txt", 'r') as f:
        api_key = f.read()
    client = OpenAI(api_key=api_key)

    print("Made OpenAI API call.")

    response = client.responses.create(
        model="gpt-4o",
        instructions="You receive an example statement or theorem in LEAN 4 and output the first line of the proof of the theorem. You produce only LEAN 4 code. You produce no natural language. You produce exactly one line of LEAN 4 code.",
        input=example
    )

    res_text = response.output_text

    return clean_response(res_text)

def solve_example(statement):
    imports = """import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat"""
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


"""
Makes a given model try the same problem `allowed_attempts` times, or until it gets it right. Provides
the model with the InfoView feedback from each of its attempts. To run with a non-GPT model, create a
wrapper class for your model that supports a `get_response` method, context window should be preserved
between calls to `get_response`.
"""
def persevere(prompt, lean_init_str="", chat=Chat("You are a helpful chat assistant.", "gpt-4o"), server = LeanServer(LEAN_CONFIG), allowed_attempts=10, print_progress=False):
    start = time.time()
    response = clean_response(chat.get_response(lean_init_str + "\n" + prompt))
    if print_progress:
        print("=====ATTEMPT 1======")
        print(response)
    # messages = server.run(Command(cmd=lean_init_str + "\n" + prompt + "\n" + response)).messages
    messages = server.run(Command(cmd=response)).messages
    # print(lean_init_str + "\n" + prompt + "\n" + response)
    for i in range(allowed_attempts - 1):
        if len(messages) == 1 and messages[0].data == "Goals accomplished!":
            print("SUCCEEDED in " + str(i + 1) + " attempt(s).")
            print("SUCCEEDED after " + str(time.time() - start) + " seconds.")
            return response
        reply = generate_reply(messages)
        if print_progress:
            print(reply)
        response = clean_response(chat.get_response(reply))
        if print_progress:
            print("=====ATTEMPT " + str(i + 2) + "=====")
            print(response)
        # messages = server.run(Command(cmd=lean_init_str + "\n" + prompt + "\n" + response)).messages
        messages = server.run(Command(cmd=response)).messages
    if print_progress:
        print("FAILED in " + str(allowed_attempts) + " attempt(s).")
        print("FAILED after " + str(time.time() - start) + " seconds.")


if __name__ == "__main__":
    # print(solve_example("""theorem mathd_numbertheory_35 (S : Finset ℕ) (h₀ : ∀ n : ℕ, n ∣ Nat.sqrt 196) : (∑ k in S, k) = 24 := by"""))
    chat = Chat("You are given a LEAN 4 example statement or theorem and you solve it. You produce LEAN 4 code. You rewrite the imports and the theorem or example statement exactly as they were given at the beginning of your proof. You do NOT import anything new. You may use natural language to think through your method. If your code doesn't work you will be given all of the messages from the LEAN 4 compiler. You will rewrite the given lines to avoid those issues.", "gpt-4o")
    persevere("""theorem mathd_algebra_22a : Real.logb (5 ^ 2) (5 ^ 4) = 2 := by""", MINIF2F_INIT_STR, chat=chat, allowed_attempts=5, print_progress=True)
    
