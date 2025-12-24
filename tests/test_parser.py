"""Unit tests for Vyra parser."""

import pytest
from vyra.parser import VyraParser
from vyra.ast_nodes import *


class TestParser:
    """Test the Vyra parser"""
    
    def setup_method(self):
        self.parser = VyraParser()
    
    def test_simple_assignment(self):
        """Test parsing simple variable assignment"""
        code = "Set x to 5."
        ast = self.parser.parse(code)
        
        assert isinstance(ast, ProgramNode)
        assert len(ast.statements) == 1
        
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.variable_name == "x"
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.value == 5
    
    def test_display_output(self):
        """Test parsing display statement"""
        code = 'Display "Hello, World!".'
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, OutputNode)
        assert len(stmt.expressions) == 1
        assert isinstance(stmt.expressions[0], LiteralNode)
        assert stmt.expressions[0].value == "Hello, World!"
    
    def test_user_input(self):
        """Test parsing input statement"""
        code = "Ask the user for their name and store it in username."
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, InputNode)
        assert stmt.variable_name == "username"
    
    def test_arithmetic_operations(self):
        """Test parsing arithmetic operations"""
        code = "Add 5 and 10 and store the result in sum."
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.variable_name == "sum"
        assert isinstance(stmt.value, BinaryOpNode)
        assert stmt.value.operator == "+"
    
    def test_if_statement(self):
        """Test parsing if statement"""
        code = """
If x is greater than 10:
  Display "Big number".
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatementNode)
        assert isinstance(stmt.condition, ComparisonNode)
        assert stmt.condition.operator == ">"
        assert len(stmt.then_block) == 1
    
    def test_while_loop(self):
        """Test parsing while loop"""
        code = """
While x is less than 100:
  Multiply x by 2.
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileLoopNode)
        assert isinstance(stmt.condition, ComparisonNode)
        assert len(stmt.body) == 1
    
    def test_for_loop(self):
        """Test parsing for-each loop"""
        code = """
For each item in list:
  Display item.
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, ForLoopNode)
        assert stmt.iterator_var == "item"
        assert len(stmt.body) == 1
    
    def test_repeat_loop(self):
        """Test parsing repeat N times loop"""
        code = """
Repeat 10 times:
  Display "Hello".
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, RepeatLoopNode)
        assert isinstance(stmt.count, LiteralNode)
        assert stmt.count.value == 10
    
    def test_increment_decrement(self):
        """Test parsing increment/decrement"""
        code = """
Increment counter.
Decrement remaining.
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 2
        assert isinstance(ast.statements[0], AssignmentNode)
        assert isinstance(ast.statements[1], AssignmentNode)
    
    def test_string_concatenation(self):
        """Test parsing string concatenation with 'followed by'"""
        code = 'Display "Hello, " followed by name followed by "!".'
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, OutputNode)
        assert len(stmt.expressions) == 3
    
    def test_list_creation(self):
        """Test parsing list literal"""
        code = "Create a list called numbers with values [1, 2, 3, 4, 5]."
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentNode)
        assert stmt.variable_name == "numbers"
        assert isinstance(stmt.value, LiteralNode)
        assert stmt.value.node_type == NodeType.LIST
    
    def test_comments(self):
        """Test that comments are ignored"""
        code = """
# This is a comment
Set x to 5.
Note: This is also a comment
Display x.
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 2
        assert isinstance(ast.statements[0], AssignmentNode)
        assert isinstance(ast.statements[1], OutputNode)
    
    def test_file_operations(self):
        """Test parsing file I/O"""
        code = """
Read file "data.txt" into content.
Write text to file "output.txt".
        """
        ast = self.parser.parse(code)
        
        assert len(ast.statements) == 2
        assert isinstance(ast.statements[0], FileReadNode)
        assert isinstance(ast.statements[1], FileWriteNode)
    
    def test_complex_program(self):
        """Test parsing a complete program"""
        code = """
Display "Enter a number:".
Ask the user for a number called num.

If num is greater than 0:
  Display "Positive".
Otherwise:
  Display "Non-positive".

Set i to 1.
While i is less than or equal to 5:
  Display the value of i.
  Increment i.
        """
        ast = self.parser.parse(code)

        assert len(ast.statements) == 5
        assert isinstance(ast.statements[0], OutputNode)
        assert isinstance(ast.statements[1], InputNode)
        assert isinstance(ast.statements[2], IfStatementNode)
        assert isinstance(ast.statements[3], AssignmentNode)
        assert isinstance(ast.statements[4], WhileLoopNode)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
