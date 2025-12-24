from io import StringIO
import sys

import pytest

from vyra.loader import load_source, IncludeError
from vyra.parser import VyraParser
from vyra.logic_graph import LogicGraph
from vyra.interpreter import VyraInterpreter


def _run(code: str, *, env: dict | None = None) -> str:
    parser = VyraParser()
    ast = parser.parse(code)
    assert not parser.errors, f"Parse errors: {parser.errors}"

    graph = LogicGraph()
    graph.from_ast(ast)

    if env:
        import os
        old = {k: os.environ.get(k) for k in env.keys()}
        os.environ.update({k: str(v) for k, v in env.items()})
    else:
        old = None

    interpreter = VyraInterpreter()
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        interpreter.execute(graph)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        if old is not None:
            import os
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


def test_include_expands_and_executes(tmp_path):
    lib = tmp_path / "lib.vyra"
    main = tmp_path / "main.vyra"

    lib.write_text('Set x to 5.\n', encoding='utf-8')
    main.write_text('Include "lib.vyra".\nDisplay the value of x.\n', encoding='utf-8')

    src = load_source(main)
    assert 'Set x to 5.' in src.text

    out = _run(src.text)
    assert '5' in out


def test_include_cycle_detected(tmp_path):
    a = tmp_path / "a.vyra"
    b = tmp_path / "b.vyra"

    a.write_text('Include "b.vyra".\n', encoding='utf-8')
    b.write_text('Include "a.vyra".\n', encoding='utf-8')

    with pytest.raises(IncludeError):
        load_source(a)


def test_include_supports_intent_extension_for_backcompat(tmp_path):
    lib = tmp_path / "lib.intent"
    main = tmp_path / "main.vyra"

    lib.write_text('Set y to 7.\n', encoding='utf-8')
    main.write_text('Include "lib.intent".\nDisplay the value of y.\n', encoding='utf-8')

    src = load_source(main)
    out = _run(src.text)
    assert '7' in out


def test_py_call_disabled_by_default_raises():
    code = 'Set r to call py_call with "math" and "sqrt" and 16.\n'
    parser = VyraParser()
    ast = parser.parse(code)
    assert not parser.errors

    graph = LogicGraph()
    graph.from_ast(ast)

    interpreter = VyraInterpreter()
    with pytest.raises(RuntimeError):
        interpreter.execute(graph)


def test_py_call_allowlisted_math_sqrt(monkeypatch):
    monkeypatch.setenv('VYRA_PY_BRIDGE', '1')
    monkeypatch.setenv('VYRA_PY_ALLOW', 'math')

    out = _run(
        'Set r to call py_call with "math" and "sqrt" and 16.\n'
        'Display the value of r.\n'
    )

    assert '4' in out
