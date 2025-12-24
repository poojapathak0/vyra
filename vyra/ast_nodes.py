"""AST Node Definitions for Vyra.

These nodes represent the abstract syntax tree after parsing.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from enum import Enum


class NodeType(Enum):
    """Types of AST nodes"""
    # Literals
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    NULL = "null"
    LIST = "list"
    DICT = "dict"
    
    # Variables
    VARIABLE = "variable"
    ASSIGNMENT = "assignment"
    
    # Operations
    BINARY_OP = "binary_op"
    UNARY_OP = "unary_op"
    COMPARISON = "comparison"
    LOGICAL_OP = "logical_op"
    
    # Control Flow
    IF_STATEMENT = "if_statement"
    WHILE_LOOP = "while_loop"
    FOR_LOOP = "for_loop"
    REPEAT_LOOP = "repeat_loop"
    BREAK = "break"
    CONTINUE = "continue"
    
    # Functions
    FUNCTION_DEF = "function_def"
    FUNCTION_CALL = "function_call"
    RETURN = "return"
    
    # I/O
    INPUT = "input"
    OUTPUT = "output"
    
    # File Operations
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    
    # Data Structures
    LIST_ACCESS = "list_access"
    LIST_APPEND = "list_append"
    DICT_ACCESS = "dict_access"
    DICT_SET = "dict_set"
    
    # Program
    PROGRAM = "program"
    BLOCK = "block"


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    node_type: NodeType
    line_number: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.node_type})"


@dataclass
class LiteralNode(ASTNode):
    """Literal values (numbers, strings, booleans)"""
    value: Any = None
    
    def __repr__(self):
        return f"Literal({self.value})"


@dataclass
class VariableNode(ASTNode):
    """Variable reference"""
    name: str = ""
    
    def __repr__(self):
        return f"Variable({self.name})"


@dataclass
class AssignmentNode(ASTNode):
    """Variable assignment: Set x to 5"""
    variable_name: str = ""
    value: ASTNode = None
    
    def __repr__(self):
        return f"Assignment({self.variable_name} = {self.value})"


@dataclass
class BinaryOpNode(ASTNode):
    """Binary operations: add, subtract, multiply, divide"""
    operator: str = ""  # +, -, *, /, %, **
    left: ASTNode = None
    right: ASTNode = None
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"


@dataclass
class ComparisonNode(ASTNode):
    """Comparison: x is greater than 5"""
    operator: str = ""  # ==, !=, <, >, <=, >=
    left: ASTNode = None
    right: ASTNode = None
    
    def __repr__(self):
        return f"Comparison({self.left} {self.operator} {self.right})"


@dataclass
class LogicalOpNode(ASTNode):
    """Logical operations: and, or, not"""
    operator: str = ""  # and, or, not
    operands: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"LogicalOp({self.operator} {self.operands})"


@dataclass
class IfStatementNode(ASTNode):
    """If-else statement"""
    condition: ASTNode = None
    then_block: List[ASTNode] = field(default_factory=list)
    else_block: List[ASTNode] = field(default_factory=list)
    elif_branches: List[tuple] = field(default_factory=list)  # [(condition, block), ...]
    
    def __repr__(self):
        return f"If({self.condition})"


@dataclass
class WhileLoopNode(ASTNode):
    """While loop"""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"While({self.condition})"


@dataclass
class ForLoopNode(ASTNode):
    """For-each loop"""
    iterator_var: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"For({self.iterator_var} in {self.iterable})"


@dataclass
class RepeatLoopNode(ASTNode):
    """Repeat N times loop"""
    count: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"Repeat({self.count})"


@dataclass
class FunctionDefNode(ASTNode):
    """Function definition"""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"FunctionDef({self.name}({', '.join(self.parameters)}))"


@dataclass
class FunctionCallNode(ASTNode):
    """Function call"""
    function_name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"FunctionCall({self.function_name})"


@dataclass
class ReturnNode(ASTNode):
    """Return statement"""
    value: Optional[ASTNode] = None
    
    def __repr__(self):
        return f"Return({self.value})"


@dataclass
class InputNode(ASTNode):
    """Get user input"""
    prompt: str = ""
    variable_name: Optional[str] = None
    input_type: str = "string"  # string, number, password
    
    def __repr__(self):
        return f"Input({self.prompt})"


@dataclass
class OutputNode(ASTNode):
    """Display output"""
    expressions: List[ASTNode] = field(default_factory=list)
    newline: bool = True
    
    def __repr__(self):
        return f"Output({len(self.expressions)} items)"


@dataclass
class FileReadNode(ASTNode):
    """Read from file"""
    filepath: ASTNode = None
    variable_name: str = ""
    mode: str = "text"  # text, json, binary
    
    def __repr__(self):
        return f"FileRead({self.filepath})"


@dataclass
class FileWriteNode(ASTNode):
    """Write to file"""
    filepath: ASTNode = None
    content: ASTNode = None
    mode: str = "text"  # text, json, binary, append
    
    def __repr__(self):
        return f"FileWrite({self.filepath})"


@dataclass
class ListAccessNode(ASTNode):
    """Access list element"""
    list_var: ASTNode = None
    index: ASTNode = None
    
    def __repr__(self):
        return f"ListAccess({self.list_var}[{self.index}])"


@dataclass
class ListAppendNode(ASTNode):
    """Append to list"""
    list_var: ASTNode = None
    value: ASTNode = None
    
    def __repr__(self):
        return f"ListAppend({self.list_var}.append({self.value}))"


@dataclass
class DictAccessNode(ASTNode):
    """Access dictionary value"""
    dict_var: ASTNode = None
    key: ASTNode = None
    
    def __repr__(self):
        return f"DictAccess({self.dict_var}[{self.key}])"


@dataclass
class DictSetNode(ASTNode):
    """Set dictionary value"""
    dict_var: ASTNode = None
    key: ASTNode = None
    value: ASTNode = None
    
    def __repr__(self):
        return f"DictSet({self.dict_var}[{self.key}] = {self.value})"


@dataclass
class BlockNode(ASTNode):
    """Block of statements"""
    statements: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"


@dataclass
class ProgramNode(ASTNode):
    """Root program node"""
    statements: List[ASTNode] = field(default_factory=list)
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


@dataclass
class BreakNode(ASTNode):
    """Break from loop"""
    pass


@dataclass
class ContinueNode(ASTNode):
    """Continue to next iteration"""
    pass
