import json
import re
from pathlib import Path

RUNS = 3
LEVELS = [1, 2, 3, 4, 5]
CASES = [1, 2, 3, 4, 5]
RESULTS_DIR = Path("results/groq")

# A fenced code block: ```typescript ... ```
FENCE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)


def extract(raw_response: str) -> str:
    """Return the code in an LLM response, unchanged.

    One fenced block: the text inside it. No fenced block: the whole response.
    More than one block: stop, because choosing between them would be a judgement.
    """
    blocks = FENCE.findall(raw_response)
    if len(blocks) == 1:
        return blocks[0]
    if len(blocks) == 0:
        return raw_response
    raise ValueError(f"{len(blocks)} code blocks in one response")


def run() -> None:
    fenced = 0
    unfenced = 0

    for level in LEVELS:
        for case in CASES:
            for run_number in range(1, RUNS + 1):
                in_path = RESULTS_DIR / f"level_{level}" / f"case_{case}_run_{run_number}.json"
                out_path = in_path.with_suffix(".ts")

                record = json.loads(in_path.read_text(encoding="utf-8"))
                raw_response = record["raw_response"]

                try:
                    code = extract(raw_response)
                except ValueError as error:
                    raise SystemExit(f"{in_path}: {error}")

                # The extracted code is a contiguous part of the response; nothing is added.
                assert code in raw_response

                if code == raw_response:
                    unfenced += 1
                else:
                    fenced += 1

                out_path.write_text(code, encoding="utf-8")
                print(f"Saved -> {out_path}")

    print(f"{fenced + unfenced} files: {fenced} from a fenced block, {unfenced} whole response")


if __name__ == "__main__":
    run()
