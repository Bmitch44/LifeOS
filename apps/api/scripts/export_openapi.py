import json
from pathlib import Path

from app.main import create_app


def main() -> None:
    app = create_app()
    schema = app.openapi()
    out = Path(__file__).resolve().parents[3] / "packages" / "shared-contracts" / "openapi" / "openapi.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(schema, indent=2))
    print(f"Wrote OpenAPI to {out}")


if __name__ == "__main__":
    main()


