from __future__ import annotations

import argparse
import json
from pathlib import Path
from .core import evaluate, load_case


def main() -> int:
    parser = argparse.ArgumentParser(description="Screen an orbital deployment case")
    parser.add_argument("case", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    body = json.dumps(evaluate(load_case(args.case)), indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body, encoding="utf-8")
    else: print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
