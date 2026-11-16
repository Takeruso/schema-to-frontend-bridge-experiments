"""Turn evaluation/validator_inputs.txt (CrossHair) into JSON bodies with Pydantic's result."""
import importlib
import json
import math
import warnings

from pydantic import ValidationError

SRC = "evaluation/validator_inputs.txt"
DST = "evaluation/validator_cases.jsonl"
MAX_SAFE = 2**53 - 1
COMPARE_OUTPUT = {(4, 1), (4, 3), (4, 4), (4, 5)}

warnings.simplefilter("ignore")

# function name -> (level, case, class, how to build the JSON body from the arguments)
TARGETS = {
    "capitalize": (4, 1, "Model", lambda _, v: {"f1": v, "f2": v}),
    "is_even": (4, 2, "Model", lambda _, v: {"number": v}),
    "ensure_list": (4, 3, "Model", lambda _, v: {"numbers": v}),
    "double_number": (4, 4, "Model", lambda _, v: {"number": v}),
    "val_number": (4, 5, "Model", lambda _, v: {"number": v}),
    "check_card_number_not_present": (
        5, 2, "UserModel",
        lambda _, d: {"username": "u", **d} if isinstance(d, dict) else d,
    ),
    "l5c1": (5, 1, "UserModel", lambda u, p, r: {"username": u, "password": p, "password_repeat": r}),
    "l5c3": (5, 3, "UserModel", lambda p, r: {"password": p, "password_repeat": r, "username": "u"}),
    "l5c4": (5, 4, "Square", lambda w, h: {"width": w, "height": h}),
    "l5c5": (
        5, 5, "Organization",
        lambda f, ps: {"forbidden_passwords": f, "users": [{"username": "u", "password": p} for p in ps]},
    ),
}


def leaves(value):
    if isinstance(value, list):
        for item in value:
            yield from leaves(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from leaves(item)
    else:
        yield value


def sendable(body):
    for v in leaves(body):
        if isinstance(v, bool):
            continue
        if isinstance(v, float) and not math.isfinite(v):
            return "nan_or_inf"
        if isinstance(v, int) and abs(v) > MAX_SAFE:
            return "unsafe_integer"
    return None


def validate(model, text, strict):
    try:
        return model.model_validate_json(text, strict=strict)
    except ValidationError:
        return None


env = {"__builtins__": {"float": float}, "Model": None, "UserModel": None}
for name in TARGETS:
    env[name] = lambda *args: args

candidates = []
for line in open(SRC):
    line = line.strip()
    if not line or line.startswith("=="):
        continue
    name = line.split("(", 1)[0]
    level, case, cls, build = TARGETS[name]
    candidates.append((level, case, cls, "crosshair", line, build(*eval(line, env))))

seen = set()
dropped = {"nan_or_inf": 0, "unsafe_integer": 0, "coercion": 0, "duplicate": 0}
rows = []
for level, case, cls, source, call, body in candidates:
    reason = sendable(body)
    if reason:
        dropped[reason] += 1
        continue
    text = json.dumps(body)
    key = (level, case, cls, json.dumps(body, sort_keys=True))
    if key in seen:
        dropped["duplicate"] += 1
        continue
    seen.add(key)
    model = getattr(importlib.import_module(f"benchmark.level_{level}.case_{case}"), cls)
    result = validate(model, text, None)
    if (result is None) != (validate(model, text, True) is None):
        dropped["coercion"] += 1
        continue
    rows.append({
        "level": level,
        "case": case,
        "path": f"/{cls}",
        "source": source,
        "call": call,
        "body": body,
        "status": 200 if result is not None else 422,
        "output": json.loads(result.model_dump_json()) if result is not None else None,
        "compare_output": (level, case) in COMPARE_OUTPUT,
    })

with open(DST, "w") as out:
    for row in rows:
        out.write(json.dumps(row, sort_keys=True) + "\n")

print("candidates", len(candidates))
print("dropped", dropped)
print("kept", len(rows))
for key in sorted({(r["level"], r["case"]) for r in rows}):
    group = [r for r in rows if (r["level"], r["case"]) == key]
    print(key, "accept", sum(r["status"] == 200 for r in group), "reject", sum(r["status"] == 422 for r in group))