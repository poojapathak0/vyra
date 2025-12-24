"""
Integration tests for IntentLang
Tests complete programs from parsing to execution
"""

import pytest
from io import StringIO
import sys
from intentlang.parser import IntentParser
from intentlang.logic_graph import LogicGraph
from intentlang.interpreter import IntentInterpreter


class TestIntegration:
    """Integration tests for complete programs"""
    
    def setup_method(self):
        self.parser = IntentParser()
        self.interpreter = IntentInterpreter()
    
    def execute_code(self, code: str, inputs: list = None) -> tuple:
        """Helper to execute code and capture output"""
        # Parse
        ast = self.parser.parse(code)
        assert not self.parser.errors, f"Parse errors: {self.parser.errors}"
        
        # Build graph
        graph = LogicGraph()
        graph.from_ast(ast)
        
        # Mock input if provided
        if inputs:
            input_iter = iter(inputs)
            original_input = __builtins__.input
            __builtins__.input = lambda prompt="": next(input_iter)
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Execute
            result = self.interpreter.execute(graph)
            output = sys.stdout.getvalue()
            return output, result
        finally:
            sys.stdout = old_stdout
            if inputs:
                __builtins__.input = original_input
    
    def test_simple_arithmetic(self):
        """Test simple arithmetic operations"""
        code = """
Set a to 5.
Set b to 10.
Add a and b and store the result in sum.
Display the value of sum.
        """
        output, result = self.execute_code(code)
        assert "15" in output
    
    def test_conditionals(self):
        """Test if-else statements"""
        code = """
Set x to 15.
If x is greater than 10:
  Display "Big".
Otherwise:
  Display "Small".
        """
        output, result = self.execute_code(code)
        assert "Big" in output
    
    def test_while_loop(self):
        """Test while loop"""
        code = """
Set i to 1.
Set sum to 0.
While i is less than or equal to 5:
  Add i to sum.
  Increment i.
Display the value of sum.
        """
        output, result = self.execute_code(code)
        assert "15" in output  # 1+2+3+4+5 = 15
    
    def test_for_loop(self):
        """Test for-each loop"""
        code = """
Create a list called numbers with values [1, 2, 3].
Set sum to 0.
For each num in numbers:
  Add num to sum.
Display the value of sum.
        """
        output, result = self.execute_code(code)
        assert "6" in output  # 1+2+3 = 6
    
    def test_repeat_loop(self):
        """Test repeat N times"""
        code = """
Set counter to 0.
Repeat 5 times:
  Increment counter.
Display the value of counter.
        """
        output, result = self.execute_code(code)
        assert "5" in output
    
    def test_string_concatenation(self):
        """Test string operations"""
        code = """
Set name to "Alice".
Set greeting to "Hello, " followed by name followed by "!".
Display the value of greeting.
        """
        output, result = self.execute_code(code)
        assert "Hello, Alice!" in output
    
    def test_nested_conditions(self):
        """Test nested if statements"""
        code = """
Set age to 25.
If age is greater than or equal to 18:
  If age is less than 65:
    Display "Adult".
  Otherwise:
    Display "Senior".
Otherwise:
  Display "Minor".
        """
        output, result = self.execute_code(code)
        assert "Adult" in output
    
    def test_list_operations(self):
        """Test list manipulation"""
        code = """
Create a list called items.
Add 10 to items.
Add 20 to items.
Add 30 to items.
Display the value of items.
        """
        output, result = self.execute_code(code)
        # Output should show the list
        assert "10" in output
        assert "20" in output
        assert "30" in output
    
    def test_comparison_operators(self):
        """Test various comparison operators"""
        code = """
Set a to 10.
Set b to 10.
If a is equal to b:
  Display "Equal".

If a is less than 20:
  Display "Less".

If a is greater than or equal to 10:
  Display "GTE".
        """
        output, result = self.execute_code(code)
        assert "Equal" in output
        assert "Less" in output
        assert "GTE" in output
    
    def test_break_in_loop(self):
        """Test break statement"""
        code = """
Set i to 0.
While i is less than 10:
  Increment i.
  If i is equal to 5:
    Stop the loop.
Display the value of i.
        """
        output, result = self.execute_code(code)
        assert "5" in output
    
    def test_variable_shadowing(self):
        """Test variable scoping"""
        code = """
Set x to 10.
Display the value of x.
Set x to 20.
Display the value of x.
        """
        output, result = self.execute_code(code)
        lines = output.strip().split('\n')
        assert "10" in lines[0]
        assert "20" in lines[1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
