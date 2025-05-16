import json
import os

def dump_formal_statements(jsonl_path: str, out_dir: str = "."):
    """
    Reads a JSONL file where each line is a problem dict with
    'name' and 'formal_statement' fields, and writes each
    formal_statement into a file named <name>.lean.
    """
    # Make sure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    with open(jsonl_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            name = data.get("name")
            stmt = data.get("formal_statement", "")
            if not name:
                continue  # skip entries without a name

            filename = os.path.join(out_dir, f"{name}.lean")

            # write the formal statement to the lean file
            with open(filename, 'w', encoding='utf-8') as f:
                # f.write("import Mathlib\n\n") # Uncomment if you want to import Mathlib
                f.write(stmt)

    print(f"Dumped formal statements into {out_dir!r}")

if __name__ == "__main__":
    dump_formal_statements("minif2f.jsonl", out_dir="lean_statements")
