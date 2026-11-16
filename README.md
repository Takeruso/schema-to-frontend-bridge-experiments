# Pydantic-to-Zod conversion: benchmark, outputs and evaluation

Artifacts for "Schema-to-Frontend Bridge: Preserving Pydantic Validator Logic in
LLM-Assisted Zod Schema Generation" (Takeru Sonoda and Matthew Mitchell, MODELSWARD 2027).

- **Benchmark:** 25 Pydantic examples copied from the Pydantic and FastAPI documentation,
  5 per level.
- **Pipelines:** pydantic2zod, Hey API (through FastAPI and OpenAPI), and an LLM
  (`openai/gpt-oss-120b` on Groq, 3 runs).
- **Evaluation:** the same JSON input is given to the Pydantic model and to the generated
  Zod schema. Pydantic is the reference.

| Level | Content |
|---|---|
| 1 | Basic types |
| 2 | `Field()` constraints |
| 3 | Nested models |
| 4 | `@field_validator` |
| 5 | `@model_validator` and cross-field checks |

## Results

Examples that agree with Pydantic on every input (5 per level). Printed by
`python count_results.py`.

| Pipeline | L1 | L2 | L3 | L4 | L5 | Agree | Not judged | Failed |
|---|---|---|---|---|---|---|---|---|
| Hey API | 5 | 4 | 5 | 0 | 0 | 14 | 2 | 9 |
| pydantic2zod | 5 | 0 | 3 | 0 | 1 | 9 | 2 | 14 |
| LLM run 1, 2, 3 (each) | 5 | 4 | 3 | 1 | 4 | 17 | 1 | 7 |

- **Failed:** at least one input disagrees, or the output could not be used.
- **Not judged:** no input fails, but the validator changes the value (Level 4 cases 1, 4
  and 5) and the only generated inputs are `""` and `0`, which stay the same. The change
  is therefore not tested.
- **Agree:** every other example.

## Files

| Path | Content |
|---|---|
| `benchmark/level_N/case_M.py` | The 25 examples |
| `benchmark/SOURCES.md` | Source file, version and lines of each example |
| `results/openapi/level_N/case_M.json` | OpenAPI documents from FastAPI |
| `results/hey/level_N/case_M/zod.gen.ts` | Hey API output |
| `results/pydantic2zod/level_N/case_M.ts` | pydantic2zod output (23 files) |
| `results/groq/level_N/case_M_run_K.json` | Prompt and raw LLM response |
| `results/groq/level_N/case_M_run_K.ts` | Code extracted from the response |
| `evaluation/` | Type-check log, inputs, test files, test results |

## Setup

```bash
pip install -r requirements.txt
pip install schemathesis==4.33.4 crosshair-tool==0.0.113 pytest
bun install
```

| Tool | Version |
|---|---|
| Python | 3.14.3 |
| pydantic / fastapi / pydantic2zod | 2.12.5 / 0.136.1 / 0.1.1 |
| zod / @hey-api/openapi-ts / TypeScript | 4.3.6 / 0.97.0 / 6.0.3 |
| schemathesis / crosshair-tool | 4.33.4 / 0.0.113 |

## Reproducing

### 1. Generate the Zod schemas

```bash
python generate_openapi.py
bunx @hey-api/openapi-ts -f openapi-ts.config.mjs
for l in 1 2 3 4 5; do for c in 1 2 3 4 5; do
  python -m pydantic2zod benchmark.level_$l.case_$c results/pydantic2zod/level_$l/case_$c.ts
done; done
```

- These commands reproduce the committed files byte for byte.
- pydantic2zod writes nothing for Level 2 case 1 (`KeyError: 'Decimal'`) and
  Level 3 case 2 (`KeyError: 'HttpUrl'`).

```bash
python run_benchmark_groq.py
python extract_llm_code.py
```

- Needs `GROQ_API_KEY`. Temperature 0, seed 0, 3 runs per example.
- The committed responses are from 16 November 2026.

### 2. Type check

```bash
bunx tsc --noEmit --strict --target es2022 --module esnext \
  --moduleResolution bundler --skipLibCheck \
  results/hey/level_*/case_*/zod.gen.ts \
  results/pydantic2zod/level_*/case_*.ts \
  results/groq/level_*/case_*_run_*.ts \
  > evaluation/typecheck.txt
```

Six files have errors (5 pydantic2zod, 1 LLM). They count as failed.

### 3. Generate inputs for types and constraints

```bash
rm -f evaluation/generated_cases.jsonl
for l in 1 2 3 4 5; do for c in 1 2 3 4 5; do
  LEVEL=$l CASE=$c OUT=evaluation/generated_cases.jsonl python -m pytest -q test_gen.py
done; done
python filter_cases.py
```

- `test_gen.py` records the requests that Schemathesis generates from the OpenAPI
  document, with Pydantic's answer (200 = accept, 422 = reject).
- `filter_cases.py` keeps 977 of the 1,377 rows.

### 4. Generate inputs for validators

CrossHair generates inputs from the validator code of Levels 4 and 5.

```bash
python -m crosshair cover --example_output_format eval_expression \
  --per_condition_timeout 25 benchmark.level_4.case_2.Model.is_even

python -m crosshair cover --example_output_format eval_expression \
  --coverage_type path --max_uninteresting_iterations 30 \
  --per_condition_timeout 30 crosshair_wrappers.l5c1

python build_validator_cases.py
```

- First command: Level 4 validators and Level 5 case 2.
- Second command: Level 5 cases 1, 3, 4, 5, through `crosshair_wrappers.py`.
- The output is saved in `evaluation/validator_inputs.txt`.
- `build_validator_cases.py` turns it into 120 JSON inputs.

### 5. Compare

```bash
bun test evaluation/compare.test.ts --reporter=junit --reporter-outfile=evaluation/compare.xml
bun test evaluation/validators.test.ts --reporter=junit --reporter-outfile=evaluation/validators.xml
python count_results.py
```

A test passes when `safeParse` agrees with Pydantic.

## Notes

AI use: Claude (Anthropic) was used to find and copy the documentation examples and to
write the scripts and test files.

## License

MIT. See `LICENSE` and `THIRD_PARTY_NOTICES`.
