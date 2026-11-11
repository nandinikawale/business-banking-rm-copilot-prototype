from pathlib import Path

import pytest

from rm_copilot.config import Settings
from rm_copilot.factory import build_orchestrator


@pytest.fixture
def orchestrator():
    root = Path(__file__).resolve().parents[1]
    return build_orchestrator(
        Settings(data_dir=root / "data" / "synthetic", knowledge_dir=root / "data" / "knowledge")
    )


@pytest.fixture
def customer_id(orchestrator):
    return orchestrator.tools.repository.customers().iloc[0]["customer_id"]
