"""Print the counts in the README from the two JUnit files.

python count_results.py            totals per pipeline, and a per-level summary of the examples
python count_results.py --detail   also every example with a failure

Per-level summary, for each example and pipeline:
  failed      at least one input in either file fails
  not judged  no input fails, but the validator rewrites the value and no generated input
              has a Pydantic output that differs from the input, so the rewrite is not tested
  agree       everything else
"""
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

FILES = ["evaluation/compare.xml", "evaluation/validators.xml"]
CASES = "evaluation/validator_cases.jsonl"
PIPELINES = ["hey", "pydantic2zod", "llm_run_1", "llm_run_2", "llm_run_3"]
DETAIL = "--detail" in sys.argv


def line(label, c):
    return f"  {label:42} not_loaded {c['not_loaded']:4} disagree {c['disagree']:4} agree {c['agree']:4} total {sum(c.values()):4}"


failed = defaultdict(set)  # pipeline -> {(level, case)} with at least one failure in either file

for path in FILES:
    totals = defaultdict(lambda: {"not_loaded": 0, "disagree": 0, "agree": 0})
    groups = defaultdict(lambda: {"not_loaded": 0, "disagree": 0, "agree": 0})
    for suite in ET.parse(path).getroot().iter("testsuite"):
        name = suite.get("name")
        pipeline = name.split(" ")[0]
        if pipeline not in PIPELINES:
            continue
        _, level, case, _ = name.split(" ")
        for test in suite.findall("testcase"):
            if test.find("failure") is None:
                kind = "agree"
            elif test.get("assertions") == "0":
                kind = "not_loaded"
            else:
                kind = "disagree"
            totals[pipeline][kind] += 1
            groups[name][kind] += 1
            if kind != "agree":
                failed[pipeline].add((int(level[6:]), int(case[5:])))
    print(path)
    for pipeline in PIPELINES:
        print(line(pipeline, totals[pipeline]))
        if DETAIL:
            for name, c in groups.items():
                if name.startswith(pipeline + " ") and (c["not_loaded"] or c["disagree"]):
                    print("  " + line(name.split(" ", 1)[1], c))

rewrites, observed = set(), set()
for row in map(json.loads, open(CASES)):
    if row["compare_output"]:
        key = (row["level"], row["case"])
        rewrites.add(key)
        if row["status"] == 200 and row["output"] != row["body"]:
            observed.add(key)
not_judged = rewrites - observed

print("examples per level: agree / not judged (5 per level)")
print("  not judged:", ", ".join(f"level_{l} case_{c}" for l, c in sorted(not_judged)))
for pipeline in PIPELINES:
    cells, agree_total, nj_total = [], 0, 0
    for level in range(1, 6):
        examples = [(level, case) for case in range(1, 6)]
        nj = sum(1 for e in examples if e not in failed[pipeline] and e in not_judged)
        agree = sum(1 for e in examples if e not in failed[pipeline] and e not in not_judged)
        cells.append(f"L{level} {agree}/{nj}")
        agree_total += agree
        nj_total += nj
    print(f"  {pipeline:13} " + " ".join(cells) + f"  total: agree {agree_total}, not judged {nj_total}, failed {25 - agree_total - nj_total}")