from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path = PROJECT_ROOT / "data" / "synthetic"
    knowledge_dir: Path = PROJECT_ROOT / "data" / "knowledge"
    default_month: str = "2025-12-01"
    knowledge_dimensions: int = 384


settings = Settings()
