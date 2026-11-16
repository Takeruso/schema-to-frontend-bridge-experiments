import json
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

# The benchmark uses Groq's OpenAI-compatible API directly.
API_KEY = os.environ["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-120b"
PROVIDER = "groq"
SEED = 0
RUNS = 3
LEVELS = [1, 2, 3, 4, 5]
CASES = [1, 2, 3, 4, 5]
OUTPUT_DIR = Path("results/groq")
REQUEST_DELAY_SECONDS = 10
RATE_LIMIT_RETRIES = 5

PROMPT_TEMPLATE = """
You are an expert in both Pydantic (Python) and Zod (TypeScript).

Convert the following Pydantic model to a Zod schema.
- Preserve ALL validator logic including @field_validator and @model_validator
- Use .refine() for single-field constraints
- Use .superRefine() for cross-field constraints
- Output ONLY the TypeScript/Zod code, no explanation

Pydantic model:
{pydantic_code}
""".strip()


def run() -> None:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
    )

    for level in LEVELS:
        for case in CASES:
            input_path = Path(f"benchmark/level_{level}/case_{case}.py")
            pydantic_code = input_path.read_text(encoding="utf-8")

            prompt = PROMPT_TEMPLATE.format(pydantic_code=pydantic_code)

            for run_number in range(1, RUNS + 1):
                out_path = OUTPUT_DIR / f"level_{level}" / f"case_{case}_run_{run_number}.json"

                if out_path.exists():
                    print(f"Skipping -> {out_path}")
                    continue

                print(f"Running Level {level} Case {case} run {run_number} with {MODEL}...")

                for retry_number in range(RATE_LIMIT_RETRIES + 1):
                    try:
                        response = client.chat.completions.create(
                            model=MODEL,
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You convert Pydantic models to precise Zod schemas."
                                },
                                {
                                    "role": "user",
                                    "content": prompt,
                                },
                            ],
                            temperature=0,
                            seed=SEED,
                        )
                        break
                    except RateLimitError:
                        if retry_number == RATE_LIMIT_RETRIES:
                            raise

                        wait_seconds = REQUEST_DELAY_SECONDS * (retry_number + 1)
                        print(f"Rate limit reached; retrying in {wait_seconds} seconds...")
                        time.sleep(wait_seconds)

                raw_response = response.choices[0].message.content or ""

                output = {
                    "level": level,
                    "case": case,
                    "run": run_number,
                    "provider": PROVIDER,
                    "model": MODEL,
                    "seed": SEED,
                    # what the API reports back, to confirm who served the request
                    "served_by": getattr(response, "provider", None),
                    "served_model": response.model,
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                    "raw_response": raw_response,
                }

                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(
                    json.dumps(output, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

                print(f"Saved -> {out_path}")
                time.sleep(REQUEST_DELAY_SECONDS)


if __name__ == "__main__":
    run()
