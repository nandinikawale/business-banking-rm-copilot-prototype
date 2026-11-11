import json

from rm_copilot.evaluation import evaluate


def evaluate_main() -> None:
    print(json.dumps(evaluate(), indent=2))
