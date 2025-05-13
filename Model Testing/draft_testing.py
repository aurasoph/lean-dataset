from openai import OpenAI
import os
from pantograph.server import Server
from pantograph.expr import TacticDraft

if __name__ == "__main__":
    # TODO: FIX THIS SLOPPY CRAP
    with open(".env", 'r') as f:
        api_key = f.read().split(' ')[2]
    client = OpenAI(api_key=api_key)

    root = """theorem test_theorem
      (p : Prop)
      (hp : p)
      : p := sorry"""

    response = client.responses.create(
        model="gpt-4o",
        instructions="You receive a theorem in LEAN 4 and output LEAN 4 code that replaces all instances of 'sorry' in the code."
                     "You do not output any natural language. You do not include the theorem header in your output,"
                     " only exactly the code that takes the place of the 'sorry'. Your output will be assumed to be LEAN 4 code, so do not include '```lean' before the code or '```' after it.",
        input=root
    )
    output_text = response.output_text

    # output_text = "hp"

    print(output_text)

    server = Server()
    unit, = server.load_sorry(root)
    state1 = server.goal_tactic(
        unit.goal_state,
        goal_id=0,
        tactic=TacticDraft(output_text))
    print(state1)
