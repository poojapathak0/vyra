"""
IntentLang Parser - Converts English sentences to AST
Uses pattern matching and NLP to understand natural language code
"""

import re
from typing import List, Optional, Tuple, Dict, Any
from .ast_nodes import *


class IntentParser:
    """
    Parses natural English sentences into an Abstract Syntax Tree (AST).
    Uses rule-based pattern matching with fuzzy matching for robustness.
    """
    
    def __init__(self):
        self.current_line = 0
        self.indent_stack = [0]
        self.errors = []
        
        # Action verb mappings
        self.action_patterns = self._build_action_patterns()
        
        # Operator mappings
        self.comparison_ops = {
            'is equal to': '==', 'equals': '==', 'is': '==',
            'is not equal to': '!=', 'does not equal': '!=',
            'is greater than': '>', 'is more than': '>',
            'is less than': '<',
            'is greater than or equal to': '>=',
            'is less than or equal to': '<=',
            'is at least': '>=', 'is at most': '<='
        }
        
        self.arithmetic_ops = {
            'plus': '+', 'add': '+', 'added to': '+',
            'minus': '-', 'subtract': '-', 'subtracted from': '-',
            'times': '*', 'multiply': '*', 'multiplied by': '*',
            'divided by': '/', 'divide': '/',
            'modulo': '%', 'remainder': '%', 'mod': '%',
            'to the power of': '**', 'power': '**'
        }
        
        self.logical_ops = {
            'and': 'and', 'or': 'or', 'not': 'not'
        }
    
    def _build_action_patterns(self) -> Dict[str, List[Tuple[str, str]]]:
        """Build regex patterns for action recognition"""
        return {
            # Variable creation and assignment
            'create': [
                (r'create\s+(?:a\s+)?(?:variable\s+)?(?:called\s+)?(\w+)(?:\s+with\s+value\s+(.+))?', 'create_var'),
                (r'make\s+(?:a\s+)?(?:variable\s+)?(?:called\s+)?(\w+)(?:\s+with\s+value\s+(.+))?', 'create_var'),
                (r'define\s+(\w+)\s+as\s+(.+)', 'create_var'),
            ],
            'set': [
                (r'set\s+(\w+)\s+to\s+(.+)', 'assign'),
                (r'store\s+(.+)\s+in\s+(\w+)', 'store'),
                (r'save\s+(.+)\s+as\s+(\w+)', 'store'),
                (r'(?:let\s+)?(\w+)\s*=\s*(.+)', 'assign'),
            ],
            
            # Arithmetic operations
            'arithmetic': [
                (r'add\s+(.+)\s+(?:and\s+)?(.+)\s+and\s+store\s+(?:the\s+)?(?:result\s+)?in\s+(\w+)', 'binary_op_store'),
                (r'(?:multiply|times)\s+(.+)\s+(?:and\s+|by\s+)?(.+)\s+and\s+store\s+(?:the\s+)?(?:result\s+)?in\s+(\w+)', 'binary_op_store'),
                (r'add\s+(.+)\s+to\s+(\w+)', 'add_to'),
                (r'subtract\s+(.+)\s+from\s+(\w+)', 'subtract_from'),
                (r'multiply\s+(\w+)\s+by\s+(.+)', 'multiply_by'),
                (r'divide\s+(\w+)\s+by\s+(.+)', 'divide_by'),
                (r'increment\s+(\w+)', 'increment'),
                (r'decrement\s+(\w+)', 'decrement'),
            ],
            
            # I/O operations
            'input': [
                (r'ask\s+(?:the\s+)?user\s+for\s+(?:their\s+)?(?:a\s+)?(\w+)(?:\s+and\s+store\s+it\s+in\s+(\w+))?', 'ask'),
                (r'get\s+(?:a\s+)?(\w+)\s+from\s+(?:the\s+)?user(?:\s+and\s+store\s+it\s+in\s+(\w+))?', 'get_input'),
                (r'prompt\s+for\s+(\w+)(?:\s+without\s+showing\s+it)?', 'prompt'),
            ],
            'output': [
                (r'display\s+(.+)', 'display'),
                (r'show\s+(.+)', 'display'),
                (r'print\s+(.+)', 'display'),
                (r'say\s+(.+)', 'display'),
            ],
            
            # Control flow
            'if': [
                (r'if\s+(.+?)(?:,|\s+then)?\s*:', 'if'),
                (r'when\s+(.+?)(?:,|\s+then)?\s*:', 'if'),
            ],
            'else': [
                (r'(?:otherwise|else)(?:\s+if\s+(.+?))?:', 'else'),
            ],
            'loop': [
                (r'repeat\s+(\d+)\s+times?:', 'repeat_times'),
                (r'repeat\s+while\s+(.+?):', 'while'),
                (r'while\s+(.+?):', 'while'),
                (r'loop\s+while\s+(.+?):', 'while'),
                (r'loop\s+until\s+(.+?):', 'until'),
                (r'for\s+each\s+(\w+)\s+in\s+(.+?):', 'for_each'),
            ],
            
            # Functions
            'function': [
                (r'create\s+function\s+(\w+)\s+that\s+takes\s+(.+?):', 'function_def'),
                (r'define\s+function\s+(\w+)(?:\s+with\s+parameters?\s+(.+?))?:', 'function_def'),
                (r'call\s+(\w+)(?:\s+with\s+(.+))?', 'function_call'),
                (r'run\s+(\w+)(?:\s+with\s+(.+))?', 'function_call'),
                (r'return\s+(.+)', 'return'),
                (r'return', 'return_void'),
            ],
            
            # File operations
            'file': [
                (r'read\s+file\s+(.+?)\s+into\s+(\w+)', 'read_file'),
                (r'load\s+(.+?)\s+from\s+(.+?)\s+into\s+(\w+)', 'load_file'),
                (r'write\s+(.+?)\s+to\s+file\s+(.+)', 'write_file'),
                (r'save\s+(.+?)\s+as\s+(?:JSON\s+)?to\s+(.+)', 'save_file'),
            ],
            
            # Loop control
            'control': [
                (r'(?:stop|break)(?:\s+the\s+loop)?', 'break'),
                (r'continue(?:\s+to\s+next\s+iteration)?', 'continue'),
                (r'exit(?:\s+the\s+function)?', 'return_void'),
            ],
            
            # Data structures
            'list': [
                (r'add\s+(.+?)\s+to\s+(\w+)', 'list_append'),
                (r'append\s+(.+?)\s+to\s+(\w+)', 'list_append'),
                (r'get\s+(?:item\s+)?at\s+index\s+(\d+)\s+from\s+(\w+)', 'list_get'),
                (r'the\s+length\s+of\s+(\w+)', 'list_length'),
            ],
        }
    
    def parse(self, source_code: str) -> ProgramNode:
        """
        Main entry point - parse IntentLang source code into AST
        """
        self.errors = []
        lines = source_code.strip().split('\n')
        statements = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            self.current_line = i + 1
            
            # Skip empty lines and comments
            if not line or line.startswith('#') or line.lower().startswith('note:'):
                i += 1
                continue
            
            # Parse statement
            statement, lines_consumed = self._parse_statement(lines, i)
            if statement:
                statements.append(statement)
            
            i += lines_consumed
        
        return ProgramNode(
            node_type=NodeType.PROGRAM,
            statements=statements,
            line_number=0
        )
    
    def _parse_statement(self, lines: List[str], start_idx: int) -> Tuple[Optional[ASTNode], int]:
        """Parse a single statement, potentially spanning multiple lines"""
        line = lines[start_idx].strip()
        
        # Remove trailing period if present
        if line.endswith('.'):
            line = line[:-1].strip()
        
        # Try to match action patterns
        for category, patterns in self.action_patterns.items():
            for pattern, action_type in patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Check if this is a block statement (ends with :)
                    if line.endswith(':'):
                        return self._parse_block_statement(lines, start_idx, action_type, match)
                    else:
                        return self._parse_simple_statement(line, action_type, match), 1
        
        # If no pattern matched, try to parse as expression or error
        self.errors.append(f"Line {self.current_line}: Could not understand: '{line}'")
        return None, 1
    
    def _parse_simple_statement(self, line: str, action_type: str, match) -> Optional[ASTNode]:
        """Parse non-block statements"""
        
        if action_type == 'create_var':
            var_name = match.group(1)
            value_str = match.group(2) if match.lastindex >= 2 else None
            value = self._parse_expression(value_str) if value_str else LiteralNode(NodeType.NULL, value=None)
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=var_name,
                value=value,
                line_number=self.current_line
            )
        
        elif action_type == 'assign':
            var_name = match.group(1)
            value_str = match.group(2)
            value = self._parse_expression(value_str)
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=var_name,
                value=value,
                line_number=self.current_line
            )
        
        elif action_type == 'store':
            value_str = match.group(1)
            var_name = match.group(2)
            value = self._parse_expression(value_str)
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=var_name,
                value=value,
                line_number=self.current_line
            )
        
        elif action_type == 'binary_op_store':
            left_str = match.group(1)
            right_str = match.group(2)
            result_var = match.group(3)
            
            # Determine operator from the line
            operator = '+'
            line_lower = line.lower()
            if 'multiply' in line_lower or 'times' in line_lower:
                operator = '*'
            elif 'subtract' in line_lower or 'minus' in line_lower:
                operator = '-'
            elif 'divide' in line_lower:
                operator = '/'
            
            left = self._parse_expression(left_str)
            right = self._parse_expression(right_str)
            
            binary_op = BinaryOpNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=left,
                right=right,
                line_number=self.current_line
            )
            
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=result_var,
                value=binary_op,
                line_number=self.current_line
            )
        
        elif action_type in ['add_to', 'multiply_by', 'divide_by', 'subtract_from']:
            if action_type == 'add_to':
                value_str = match.group(1)
                var_name = match.group(2)
                operator = '+'
            elif action_type == 'subtract_from':
                value_str = match.group(1)
                var_name = match.group(2)
                operator = '-'
            elif action_type == 'multiply_by':
                var_name = match.group(1)
                value_str = match.group(2)
                operator = '*'
            elif action_type == 'divide_by':
                var_name = match.group(1)
                value_str = match.group(2)
                operator = '/'
            
            var_node = VariableNode(NodeType.VARIABLE, name=var_name)
            value_node = self._parse_expression(value_str)
            
            binary_op = BinaryOpNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=var_node,
                right=value_node,
                line_number=self.current_line
            )
            
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=var_name,
                value=binary_op,
                line_number=self.current_line
            )
        
        elif action_type in ['increment', 'decrement']:
            var_name = match.group(1)
            operator = '+' if action_type == 'increment' else '-'
            
            var_node = VariableNode(NodeType.VARIABLE, name=var_name)
            one_node = LiteralNode(NodeType.NUMBER, value=1)
            
            binary_op = BinaryOpNode(
                node_type=NodeType.BINARY_OP,
                operator=operator,
                left=var_node,
                right=one_node,
                line_number=self.current_line
            )
            
            return AssignmentNode(
                node_type=NodeType.ASSIGNMENT,
                variable_name=var_name,
                value=binary_op,
                line_number=self.current_line
            )
        
        elif action_type in ['ask', 'get_input', 'prompt']:
            prompt_text = match.group(1)
            var_name = match.group(2) if match.lastindex >= 2 and match.group(2) else prompt_text
            
            # Clean up prompt text
            prompt_text = prompt_text.replace('_', ' ').replace('their ', '').replace('a ', '')
            is_password = 'password' in line.lower() and 'without showing' in line.lower()
            
            return InputNode(
                node_type=NodeType.INPUT,
                prompt=f"Enter {prompt_text}: ",
                variable_name=var_name,
                input_type='password' if is_password else 'string',
                line_number=self.current_line
            )
        
        elif action_type == 'display':
            output_str = match.group(1)
            expressions = self._parse_output_expression(output_str)
            return OutputNode(
                node_type=NodeType.OUTPUT,
                expressions=expressions,
                line_number=self.current_line
            )
        
        elif action_type == 'function_call':
            func_name = match.group(1)
            args_str = match.group(2) if match.lastindex >= 2 and match.group(2) else ""
            
            arguments = []
            if args_str:
                arg_parts = [a.strip() for a in args_str.split(' and ')]
                arguments = [self._parse_expression(arg) for arg in arg_parts]
            
            return FunctionCallNode(
                node_type=NodeType.FUNCTION_CALL,
                function_name=func_name,
                arguments=arguments,
                line_number=self.current_line
            )
        
        elif action_type == 'return':
            value_str = match.group(1)
            value = self._parse_expression(value_str)
            return ReturnNode(
                node_type=NodeType.RETURN,
                value=value,
                line_number=self.current_line
            )
        
        elif action_type == 'return_void':
            return ReturnNode(
                node_type=NodeType.RETURN,
                value=None,
                line_number=self.current_line
            )
        
        elif action_type == 'break':
            return BreakNode(node_type=NodeType.BREAK, line_number=self.current_line)
        
        elif action_type == 'continue':
            return ContinueNode(node_type=NodeType.CONTINUE, line_number=self.current_line)
        
        elif action_type == 'read_file':
            filepath_str = match.group(1)
            var_name = match.group(2)
            filepath = self._parse_expression(filepath_str)
            return FileReadNode(
                node_type=NodeType.FILE_READ,
                filepath=filepath,
                variable_name=var_name,
                line_number=self.current_line
            )
        
        elif action_type == 'write_file':
            content_str = match.group(1)
            filepath_str = match.group(2)
            content = self._parse_expression(content_str)
            filepath = self._parse_expression(filepath_str)
            return FileWriteNode(
                node_type=NodeType.FILE_WRITE,
                filepath=filepath,
                content=content,
                line_number=self.current_line
            )
        
        elif action_type == 'list_append':
            value_str = match.group(1)
            list_var = match.group(2)
            value = self._parse_expression(value_str)
            list_node = VariableNode(NodeType.VARIABLE, name=list_var)
            return ListAppendNode(
                node_type=NodeType.LIST_APPEND,
                list_var=list_node,
                value=value,
                line_number=self.current_line
            )
        
        return None
    
    def _parse_block_statement(self, lines: List[str], start_idx: int, action_type: str, match) -> Tuple[Optional[ASTNode], int]:
        """Parse block statements (if, while, for, function)"""
        
        # Find the indented block
        block_lines, lines_consumed = self._extract_block(lines, start_idx + 1)
        
        if action_type == 'if':
            condition_str = match.group(1)
            condition = self._parse_condition(condition_str)
            
            # Parse the then block
            then_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    then_statements.append(stmt)
            
            return IfStatementNode(
                node_type=NodeType.IF_STATEMENT,
                condition=condition,
                then_block=then_statements,
                line_number=self.current_line
            ), lines_consumed
        
        elif action_type == 'while':
            condition_str = match.group(1)
            condition = self._parse_condition(condition_str)
            
            body_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    body_statements.append(stmt)
            
            return WhileLoopNode(
                node_type=NodeType.WHILE_LOOP,
                condition=condition,
                body=body_statements,
                line_number=self.current_line
            ), lines_consumed
        
        elif action_type == 'until':
            condition_str = match.group(1)
            # Negate the condition for "until"
            condition = self._parse_condition(condition_str)
            # Wrap in a logical not
            condition = LogicalOpNode(
                node_type=NodeType.LOGICAL_OP,
                operator='not',
                operands=[condition]
            )
            
            body_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    body_statements.append(stmt)
            
            return WhileLoopNode(
                node_type=NodeType.WHILE_LOOP,
                condition=condition,
                body=body_statements,
                line_number=self.current_line
            ), lines_consumed
        
        elif action_type == 'repeat_times':
            count_str = match.group(1)
            count = LiteralNode(NodeType.NUMBER, value=int(count_str))
            
            body_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    body_statements.append(stmt)
            
            return RepeatLoopNode(
                node_type=NodeType.REPEAT_LOOP,
                count=count,
                body=body_statements,
                line_number=self.current_line
            ), lines_consumed
        
        elif action_type == 'for_each':
            iterator_var = match.group(1)
            iterable_str = match.group(2)
            iterable = self._parse_expression(iterable_str)
            
            body_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    body_statements.append(stmt)
            
            return ForLoopNode(
                node_type=NodeType.FOR_LOOP,
                iterator_var=iterator_var,
                iterable=iterable,
                body=body_statements,
                line_number=self.current_line
            ), lines_consumed
        
        elif action_type == 'function_def':
            func_name = match.group(1)
            params_str = match.group(2) if match.lastindex >= 2 and match.group(2) else ""
            
            parameters = []
            if params_str:
                parameters = [p.strip() for p in params_str.replace(' and ', ',').split(',')]
            
            body_statements = []
            for line in block_lines:
                stmt, _ = self._parse_statement([line], 0)
                if stmt:
                    body_statements.append(stmt)
            
            return FunctionDefNode(
                node_type=NodeType.FUNCTION_DEF,
                name=func_name,
                parameters=parameters,
                body=body_statements,
                line_number=self.current_line
            ), lines_consumed
        
        return None, lines_consumed
    
    def _extract_block(self, lines: List[str], start_idx: int) -> Tuple[List[str], int]:
        """Extract indented block of code"""
        block_lines = []
        i = start_idx
        
        # Determine base indentation
        if i < len(lines):
            first_line = lines[i]
            base_indent = len(first_line) - len(first_line.lstrip())
        else:
            return block_lines, 1
        
        # Collect all lines with greater or equal indentation
        while i < len(lines):
            line = lines[i]
            if not line.strip():  # Skip empty lines
                i += 1
                continue
            
            current_indent = len(line) - len(line.lstrip())
            
            if current_indent < base_indent:
                break  # End of block
            
            block_lines.append(line.strip())
            i += 1
        
        return block_lines, i - start_idx + 1
    
    def _parse_expression(self, expr_str: str) -> ASTNode:
        """Parse an expression (literal, variable, operation)"""
        expr_str = expr_str.strip()
        
        # Check for literals
        # String literal
        if (expr_str.startswith('"') and expr_str.endswith('"')) or \
           (expr_str.startswith("'") and expr_str.endswith("'")):
            return LiteralNode(NodeType.STRING, value=expr_str[1:-1])
        
        # Number literal
        try:
            if '.' in expr_str:
                return LiteralNode(NodeType.NUMBER, value=float(expr_str))
            else:
                return LiteralNode(NodeType.NUMBER, value=int(expr_str))
        except ValueError:
            pass
        
        # Boolean literal
        if expr_str.lower() in ['true', 'yes']:
            return LiteralNode(NodeType.BOOLEAN, value=True)
        if expr_str.lower() in ['false', 'no']:
            return LiteralNode(NodeType.BOOLEAN, value=False)
        
        # List literal
        if expr_str.startswith('[') and expr_str.endswith(']'):
            list_str = expr_str[1:-1]
            if not list_str.strip():
                return LiteralNode(NodeType.LIST, value=[])
            elements = [self._parse_expression(e.strip()) for e in list_str.split(',')]
            return LiteralNode(NodeType.LIST, value=elements)
        
        # Check for binary operations in natural language
        for op_phrase, op_symbol in self.arithmetic_ops.items():
            if op_phrase in expr_str.lower():
                parts = re.split(re.escape(op_phrase), expr_str, flags=re.IGNORECASE, maxsplit=1)
                if len(parts) == 2:
                    left = self._parse_expression(parts[0].strip())
                    right = self._parse_expression(parts[1].strip())
                    return BinaryOpNode(
                        node_type=NodeType.BINARY_OP,
                        operator=op_symbol,
                        left=left,
                        right=right
                    )
        
        # Check for "the value of x" pattern
        value_match = re.match(r'the\s+value\s+of\s+(\w+)', expr_str, re.IGNORECASE)
        if value_match:
            return VariableNode(NodeType.VARIABLE, name=value_match.group(1))
        
        # Check for "x followed by y" pattern (string concatenation)
        if ' followed by ' in expr_str:
            parts = expr_str.split(' followed by ')
            if len(parts) >= 2:
                result = self._parse_expression(parts[0].strip())
                for part in parts[1:]:
                    right = self._parse_expression(part.strip())
                    result = BinaryOpNode(
                        node_type=NodeType.BINARY_OP,
                        operator='+',
                        left=result,
                        right=right
                    )
                return result
        
        # Default to variable reference
        return VariableNode(NodeType.VARIABLE, name=expr_str)
    
    def _parse_condition(self, cond_str: str) -> ASTNode:
        """Parse a condition expression"""
        cond_str = cond_str.strip()
        
        # Check for logical operators
        for op_phrase, op_symbol in self.logical_ops.items():
            if f' {op_phrase} ' in cond_str.lower():
                parts = re.split(rf'\s+{re.escape(op_phrase)}\s+', cond_str, flags=re.IGNORECASE, maxsplit=1)
                if len(parts) == 2:
                    left = self._parse_condition(parts[0].strip())
                    right = self._parse_condition(parts[1].strip())
                    return LogicalOpNode(
                        node_type=NodeType.LOGICAL_OP,
                        operator=op_symbol,
                        operands=[left, right]
                    )
        
        # Check for comparison operators
        for op_phrase, op_symbol in self.comparison_ops.items():
            if op_phrase in cond_str.lower():
                parts = re.split(re.escape(op_phrase), cond_str, flags=re.IGNORECASE, maxsplit=1)
                if len(parts) == 2:
                    left = self._parse_expression(parts[0].strip())
                    right = self._parse_expression(parts[1].strip())
                    return ComparisonNode(
                        node_type=NodeType.COMPARISON,
                        operator=op_symbol,
                        left=left,
                        right=right
                    )
        
        # Default: treat as boolean expression
        return self._parse_expression(cond_str)
    
    def _parse_output_expression(self, output_str: str) -> List[ASTNode]:
        """Parse output expression which may contain multiple parts"""
        # Handle "followed by" concatenation
        if ' followed by ' in output_str:
            parts = output_str.split(' followed by ')
            return [self._parse_expression(part.strip()) for part in parts]
        
        # Single expression
        return [self._parse_expression(output_str)]
