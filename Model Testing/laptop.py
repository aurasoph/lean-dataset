from fastapi import FastAPI, Request
import uvicorn
from lean_interact import LeanREPLConfig, TempRequireProject, LeanRequire, LeanServer, FileCommand, Command
import lean_ai_tools

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

lean_server = LeanServer(LEAN_CONFIG)

app = FastAPI()

@app.post("/ping")
async def ping():
    return {"message" : "pong"}

@app.post("/lean-response")
async def compile_request(request: Request):
    res = await request.json()
    data = res["lean"]
    result = lean_server.run(Command(cmd=data))
    if len(result) == 1 and result[0].data == "Goals accomplished!":
        return {"message" : ""}
    return {"message" : lean_ai_tools.generate_reply(result.messages)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
