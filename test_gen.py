import json, os
import schemathesis
from fastapi import FastAPI
from generate_openapi import add_model_routes

LEVEL, CASE = os.environ["LEVEL"], os.environ["CASE"]
app = FastAPI()
add_model_routes(app, f"benchmark.level_{LEVEL}.case_{CASE}")
schema = schemathesis.openapi.from_asgi("/openapi.json", app)
OUT = open(os.environ["OUT"], "a")

@schema.parametrize()
def test_api(case):
    resp = case.call()
    d = case.meta.phase.data
    body = None if type(case.body).__name__ == "NotSet" else case.body
    OUT.write(json.dumps({
        "level": int(LEVEL), "case": int(CASE), "path": case.path, "method": case.method,
        "scenario": d.scenario.value, "description": d.description, "location": d.location,
        "body": body, "status": resp.status_code,
    }, sort_keys=True, default=str) + "\n")