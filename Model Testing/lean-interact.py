#%%
from lean_interact import LeanREPLConfig, TempRequireProject, LeanRequire, LeanServer, FileCommand, Command
from pathlib import Path
import re
# Create a temporary project with Mathlib as a dependency
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

class eval:
    def __init__(self, path):
        server = LeanServer(config)
        self.path = Path(path).resolve()

        response = server.run(FileCommand(path=str(self.path)))
        self.response = response
        count = 0
        tot = 0
        errors = []
        for x in response.messages:
            if (x.severity == "error" and re.search("unsolved goals", x.data)) or (x.severity == "warning" and re.search("sorry", x.data)): 
                tot+=1
                errors.append(x)
            if x.severity == "info" and re.search("Goals accomplished", x.data): 
                count+=1
                tot+=1
        self.errors = errors
        self.accuracy = count/tot







#%%