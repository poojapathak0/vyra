"""Vyra source loader.

Supports multi-file programs via `Include "relative/path.vyra".` lines.

Note: `.vyra` is the recommended file extension. `.intent` is still supported for backward compatibility.

This is a pre-parse expansion step used by the CLI.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set


_INCLUDE_RE = re.compile(r"^\s*include\s+[\"'](.+?)[\"']\s*\.?\s*$", re.IGNORECASE)


class IncludeError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceFile:
    path: Path
    text: str


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise IncludeError(f"Included file not found: {path}") from e


def expand_includes(text: str, *, base_dir: Path, _stack: List[Path] | None = None) -> str:
    """Expand Include statements recursively.

    - `base_dir` is the directory for resolving relative include paths.
    - Cycle detection is enforced using `_stack`.
    """

    stack: List[Path] = list(_stack or [])
    expanded_lines: List[str] = []

    for raw_line in text.splitlines():
        match = _INCLUDE_RE.match(raw_line)
        if not match:
            expanded_lines.append(raw_line)
            continue

        rel = match.group(1).strip()
        include_path = (base_dir / rel).resolve()

        if include_path in stack:
            cycle = " -> ".join([str(p) for p in stack + [include_path]])
            raise IncludeError(f"Include cycle detected: {cycle}")

        stack.append(include_path)
        included_text = _read_text(include_path)
        expanded = expand_includes(included_text, base_dir=include_path.parent, _stack=stack)
        expanded_lines.append(expanded)
        stack.pop()

    return "\n".join(expanded_lines) + ("\n" if text.endswith("\n") else "")


def load_source(entry_file: str | Path) -> SourceFile:
    """Load a Vyra program from a file, expanding includes."""

    path = Path(entry_file).expanduser().resolve()
    text = _read_text(path)
    expanded = expand_includes(text, base_dir=path.parent, _stack=[path])
    return SourceFile(path=path, text=expanded)
