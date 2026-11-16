import json
import importlib
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

LEVELS = [1, 2, 3, 4, 5]
CASES = [1, 2, 3, 4, 5]
OUTPUT_DIR = Path("results/openapi")


def add_model_routes(app: FastAPI, module_name: str) -> None:
    module = importlib.import_module(module_name)

    for name, obj in vars(module).items():
        if isinstance(obj, type) and issubclass(obj, BaseModel) and obj is not BaseModel:
            route_path = f"/{name}"

            async def endpoint(payload: obj):  # type: ignore
                return payload

            app.post(route_path, response_model=obj)(endpoint)


def main() -> None:
    Path("benchmark/__init__.py").touch()

    for level in LEVELS:
        for case in CASES:
            app = FastAPI(title=f"Benchmark Level {level} Case {case}")
            add_model_routes(app, f"benchmark.level_{level}.case_{case}")

            out_path = OUTPUT_DIR / f"level_{level}" / f"case_{case}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(
                json.dumps(app.openapi(), indent=2),
                encoding="utf-8",
            )

            print(f"Saved -> {out_path}")


if __name__ == "__main__":
    main()
