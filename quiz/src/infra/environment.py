from pathlib import Path

from dotenv import load_dotenv


# quiz/src/infra/environment.py 
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


def load_project_environment() -> None:
    """Load the repository-root environment file independently of cwd."""
    load_dotenv(ENV_FILE, override=True)


def resolve_project_path(value: str) -> Path:
    """Resolve relative paths from the repository root, preserving absolute paths."""
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path
