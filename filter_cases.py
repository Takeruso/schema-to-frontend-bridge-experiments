"""Select the rows of evaluation/generated_cases.jsonl used for the comparison.

Dropped, in this order:
  1. rows that do not send a JSON body with POST
  2. rows with an integer outside the JavaScript safe range (|n| > 2**53 - 1)
  3. rows where Pydantic's default and strict JSON validation disagree
"""
import importlib
import json

from pydantic import ValidationError

SRC = "evaluation/generated_cases.jsonl"
DST = "evaluation/body_cases.jsonl"
NOT_BODY = {
    "unspecified_http_method",
    "unsupported_content_type",
    "malformed_content_type",
    "missing_parameter",
}
MAX_SAFE = 2**53 - 1


def integers(value):
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from integers(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from integers(item)


def accepts(model, text, strict):
    try:
        model.model_validate_json(text, strict=strict)
        return True
    except ValidationError:
        return False


rows = [json.loads(line) for line in open(SRC)]
kept = []
dropped = {"not_body": 0, "unsafe_integer": 0, "coercion": 0}

for row in rows:
    if row["method"] != "POST" or row["scenario"] in NOT_BODY:
        dropped["not_body"] += 1
        continue
    if any(abs(n) > MAX_SAFE for n in integers(row["body"])):
        dropped["unsafe_integer"] += 1
        continue
    module = importlib.import_module(f"benchmark.level_{row['level']}.case_{row['case']}")
    model = getattr(module, row["path"].lstrip("/"))
    text = json.dumps(row["body"])
    default = accepts(model, text, None)
    assert default == (row["status"] == 200), row
    if default != accepts(model, text, True):
        dropped["coercion"] += 1
        continue
    kept.append(row)

with open(DST, "w") as out:
    for row in kept:
        out.write(json.dumps(row, sort_keys=True) + "\n")

print("read", len(rows))
print("dropped", dropped)
print("kept", len(kept))