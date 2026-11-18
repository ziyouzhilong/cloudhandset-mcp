#!/usr/bin/env python3
"""Bind a real, user-created OpenAI connection ID inside this unpacked package."""
import argparse
import json
from pathlib import Path
import re


def bind(connection_id, package_root):
    # The Plugins page prefixes its technical ID with plugin_; app mappings don't.
    app_id = connection_id.removeprefix("plugin_")
    if not re.fullmatch(r"asdk_app_[0-9a-f]{32}", app_id):
        raise ValueError("Expected the real asdk_app_… or plugin_asdk_app_… technical ID; no URL/token")
    path = package_root / "plugin" / ".app.json"
    if path.is_symlink():
        raise ValueError("Refusing a symlinked connection mapping")
    current = json.loads(path.read_text(encoding="utf-8"))
    target = {"apps": {"cloudhandset": {"id": app_id}}}
    if current != {"apps": {}} and current != target:
        raise ValueError("An existing connection is bound; retain it or edit the mapping explicitly")
    path.write_text(json.dumps(target, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("connection_id")
    args = parser.parse_args()
    try:
        bind(args.connection_id, Path(__file__).resolve().parent)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print("Bound this package only. Install/connect the plugin in the host to use its tools.")
