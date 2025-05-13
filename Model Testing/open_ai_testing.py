from openai import OpenAI

if __name__ == "__main__":
    # TODO: FIX THIS SLOPPY CRAP
    with open(".env", 'r') as f:
        api_key = f.read().split(' ')[2]
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a coding assistant that talks like a pirate.",
        input="How do I check if a Python object is an instance of a class?",
    )

    print(response.output_text)
