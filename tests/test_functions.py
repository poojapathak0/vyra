"""Function tests for Vyra"""

import sys
from io import StringIO

from vyra.parser import IntentParser
from vyra.logic_graph import LogicGraph
from vyra.interpreter import IntentInterpreter


class TestFunctions:
    def setup_method(self):
        self.parser = IntentParser()
        self.interpreter = IntentInterpreter()

    def execute_code(self, code: str) -> str:
        ast = self.parser.parse(code)
        assert not self.parser.errors, f"Parse errors: {self.parser.errors}"

        graph = LogicGraph()
        graph.from_ast(ast)

        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            self.interpreter.execute(graph)
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

    def test_function_return_and_store(self):
        code = """
Create function add that takes a and b:
  Return a plus b.

Call add with 10 and 20 and store the result in total.
Display the value of total.
        """
        output = self.execute_code(code)
        assert "30" in output

    def test_function_call_in_expression(self):
        code = """
Create function add that takes a and b:
  Return a plus b.

Set sum to call add with 2 and 3.
Display the value of sum.
        """
        output = self.execute_code(code)
        assert "5" in output

    def test_builtin_length(self):
        code = """
Set n to call length with [1, 2, 3].
Display the value of n.
        """
        output = self.execute_code(code)
        assert "3" in output
