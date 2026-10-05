import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEMO_USER_ID = "U001"


def _load_env() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


_load_env()


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    base_url: str
    db_url: str
    timeout_s: float = 60.0
    repeats: int = 3
    concurrency: int = 6


def settings() -> Settings:
    return Settings(
        api_key=os.environ.get("NEBIUS_API_KEY", ""),
        model=os.environ.get("NEBIUS_MODEL", ""),
        base_url=os.environ.get("NEBIUS_BASE_URL", "").rstrip("/"),
        db_url=os.environ.get(
            "RECALLGUARD_DB_URL", f"sqlite:///{ROOT / 'backend' / 'recallguard.db'}"
        ),
    )
