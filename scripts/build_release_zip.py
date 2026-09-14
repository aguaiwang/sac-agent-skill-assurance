"""Build the public distribution archive without flattening project paths."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"dist", ".pytest_cache", "__pycache__", "build", ".venv"}


def include(path: Path) -> bool:
    relative = path.relative_to(PROJECT_ROOT)
    return (
        not any(part in EXCLUDED_PARTS for part in relative.parts)
        and path.name != ".env"
        and path.suffix not in {".pyc", ".pyo"}
        and not any(part.endswith(".egg-info") for part in relative.parts)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", default="agent-skill-assurance-v1.0.0.zip")
    args = parser.parse_args()
    archive_path = PROJECT_ROOT / "dist" / args.archive
    archive_path.parent.mkdir(exist_ok=True)
    files = sorted(path for path in PROJECT_ROOT.rglob("*") if path.is_file() and include(path))
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for file in files:
            # Keep the top-level package directory and every nested path.
            archive.write(file, file.relative_to(PROJECT_ROOT.parent).as_posix())
    print(archive_path)
    print(f"files={len(files)}")


if __name__ == "__main__":
    main()
