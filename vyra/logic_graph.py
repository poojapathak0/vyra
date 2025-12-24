"""Logic Graph - Intermediate Representation for Vyra.

Converts AST to a deterministic control flow graph for execution.
"""

import json
import networkx as nx
from typing import Dict, List, Any, Optional
from .ast_nodes import *


class GraphNode:
    """Node in the logic graph"""
    
    def __init__(self, node_id: int, node_type: str, data: Dict[str, Any]):
        self.id = node_id
        self.type = node_type
        self.data = data
        self.successors = []
        self.predecessors = []
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type,
            'data': self.data,
            'successors': self.successors,
            'predecessors': self.predecessors
        }
    
    def __repr__(self):
        return f"GraphNode(id={self.id}, type={self.type})"


class LogicGraph:
    """
    Logic Graph - Intermediate Representation
    
    Represents program as a directed graph where:
    - Nodes are operations (assignments, conditionals, loops, I/O, etc.)
    - Edges represent control flow and data dependencies
    - Deterministic execution by graph traversal
    """
    
    def __init__(self):
        self.nodes: Dict[int, GraphNode] = {}
        self.edges: List[tuple] = []
        self.entry_node_id = None
        self.exit_node_id = None
        self.next_node_id = 0
        self.graph = nx.DiGraph()  # NetworkX graph for algorithms
    
    def add_node(self, node_type: str, data: Dict[str, Any]) -> GraphNode:
        """Add a node to the graph"""
        node = GraphNode(self.next_node_id, node_type, data)
        self.nodes[self.next_node_id] = node
        self.graph.add_node(self.next_node_id, type=node_type, data=data)
        self.next_node_id += 1
        return node
    
    def add_edge(self, from_node_id: int, to_node_id: int, edge_type: str = 'next'):
        """Add an edge between nodes"""
        self.edges.append((from_node_id, to_node_id, edge_type))
        self.nodes[from_node_id].successors.append(to_node_id)
        self.nodes[to_node_id].predecessors.append(from_node_id)
        self.graph.add_edge(from_node_id, to_node_id, type=edge_type)
    
    def to_dict(self) -> Dict:
        """Serialize graph to dictionary"""
        return {
            'nodes': [node.to_dict() for node in self.nodes.values()],
            'edges': [{'from': e[0], 'to': e[1], 'type': e[2]} for e in self.edges],
            'entry': self.entry_node_id,
            'exit': self.exit_node_id
        }
    
    def to_json(self) -> str:
        """Serialize graph to JSON"""
        return json.dumps(self.to_dict(), indent=2)
    
    def from_ast(self, ast: ProgramNode) -> 'LogicGraph':
        """Build logic graph from AST"""
        builder = LogicGraphBuilder(self)
        builder.build(ast)
        return self
    
    def visualize(self, output_file: str = None):
        """
        Visualize the logic graph using matplotlib/graphviz
        """
        try:
            import matplotlib.pyplot as plt
            from networkx.drawing.nx_agraph import graphviz_layout
        except ImportError:
            print("Warning: matplotlib or pygraphviz not installed. Cannot visualize.")
            return
        
        # Create layout
        try:
            pos = graphviz_layout(self.graph, prog='dot')
        except:
            pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        node_colors = []
        node_labels = {}
        for node_id, node in self.nodes.items():
            if node.type == 'entry':
                node_colors.append('lightgreen')
            elif node.type == 'exit':
                node_colors.append('lightcoral')
            elif node.type in ['if', 'while', 'for']:
                node_colors.append('lightyellow')
            else:
                node_colors.append('lightblue')
            
            # Create label
            label = f"{node.type}\n"
            if 'variable' in node.data:
                label += f"{node.data['variable']}"
            elif 'operator' in node.data:
                label += f"{node.data['operator']}"
            elif 'text' in node.data:
                text = node.data['text'][:20]
                label += f'"{text}..."' if len(node.data['text']) > 20 else f'"{text}"'
            node_labels[node_id] = label
        
        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, 
                node_color=node_colors,
                labels=node_labels,
                with_labels=True,
                node_size=1500,
                font_size=8,
                font_weight='bold',
                arrows=True,
                arrowsize=20,
                edge_color='gray',
                arrowstyle='->')
        
        plt.title("Vyra Logic Graph", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Graph visualization saved to {output_file}")
        else:
            plt.show()


class LogicGraphBuilder:
    """Builds logic graph from AST"""
    
    def __init__(self, graph: LogicGraph):
        self.graph = graph
        self.current_node_id = None
        self.break_targets = []  # Stack of break target nodes
        self.continue_targets = []  # Stack of continue target nodes
    
    def build(self, ast: ProgramNode):
        """Build graph from AST"""
        # Create entry node
        entry = self.graph.add_node('entry', {'label': 'START'})
        self.graph.entry_node_id = entry.id
        self.current_node_id = entry.id
        
        # Process all statements
        for statement in ast.statements:
            self.current_node_id = self.visit(statement, self.current_node_id)
        
        # Create exit node
        exit_node = self.graph.add_node('exit', {'label': 'END'})
        self.graph.exit_node_id = exit_node.id
        if self.current_node_id is not None:
            self.graph.add_edge(self.current_node_id, exit_node.id)
    
    def visit(self, node: ASTNode, from_node_id: int) -> int:
        """Visit AST node and add to graph. Returns ID of last created node."""
        
        if isinstance(node, AssignmentNode):
            return self.visit_assignment(node, from_node_id)
        
        elif isinstance(node, OutputNode):
            return self.visit_output(node, from_node_id)
        
        elif isinstance(node, InputNode):
            return self.visit_input(node, from_node_id)
        
        elif isinstance(node, IfStatementNode):
            return self.visit_if(node, from_node_id)
        
        elif isinstance(node, WhileLoopNode):
            return self.visit_while(node, from_node_id)
        
        elif isinstance(node, ForLoopNode):
            return self.visit_for(node, from_node_id)
        
        elif isinstance(node, RepeatLoopNode):
            return self.visit_repeat(node, from_node_id)
        
        elif isinstance(node, FunctionDefNode):
            return self.visit_function_def(node, from_node_id)
        
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node, from_node_id)
        
        elif isinstance(node, ReturnNode):
            return self.visit_return(node, from_node_id)
        
        elif isinstance(node, BreakNode):
            return self.visit_break(node, from_node_id)
        
        elif isinstance(node, ContinueNode):
            return self.visit_continue(node, from_node_id)
        
        elif isinstance(node, FileReadNode):
            return self.visit_file_read(node, from_node_id)
        
        elif isinstance(node, FileWriteNode):
            return self.visit_file_write(node, from_node_id)
        
        elif isinstance(node, ListAppendNode):
            return self.visit_list_append(node, from_node_id)
        
        return from_node_id
    
    def visit_assignment(self, node: AssignmentNode, from_node_id: int) -> int:
        """Create assignment node"""
        assign_node = self.graph.add_node('assignment', {
            'variable': node.variable_name,
            'value': self.serialize_expression(node.value),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, assign_node.id)
        return assign_node.id
    
    def visit_output(self, node: OutputNode, from_node_id: int) -> int:
        """Create output node"""
        output_node = self.graph.add_node('output', {
            'expressions': [self.serialize_expression(expr) for expr in node.expressions],
            'newline': node.newline,
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, output_node.id)
        return output_node.id
    
    def visit_input(self, node: InputNode, from_node_id: int) -> int:
        """Create input node"""
        input_node = self.graph.add_node('input', {
            'prompt': node.prompt,
            'variable': node.variable_name,
            'input_type': node.input_type,
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, input_node.id)
        return input_node.id
    
    def visit_if(self, node: IfStatementNode, from_node_id: int) -> int:
        """Create if-else structure"""
        # Create condition node
        cond_node = self.graph.add_node('if', {
            'condition': self.serialize_expression(node.condition),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, cond_node.id)

        # Create merge node
        merge_node = self.graph.add_node('merge', {'label': 'merge'})

        # THEN branch entry
        then_entry_node = self.graph.add_node('then_entry', {'label': 'then'})
        self.graph.add_edge(cond_node.id, then_entry_node.id, 'then')

        then_last = then_entry_node.id
        for stmt in node.then_block:
            then_last = self.visit(stmt, then_last)

        self.graph.add_edge(then_last, merge_node.id, 'then_exit')

        # ELSE branch entry
        if node.else_block:
            else_entry_node = self.graph.add_node('else_entry', {'label': 'else'})
            self.graph.add_edge(cond_node.id, else_entry_node.id, 'else')

            else_last = else_entry_node.id
            for stmt in node.else_block:
                else_last = self.visit(stmt, else_last)

            self.graph.add_edge(else_last, merge_node.id, 'else_exit')
        else:
            self.graph.add_edge(cond_node.id, merge_node.id, 'else_skip')

        return merge_node.id
    
    def visit_while(self, node: WhileLoopNode, from_node_id: int) -> int:
        """Create while loop structure"""
        # Create condition node
        cond_node = self.graph.add_node('while', {
            'condition': self.serialize_expression(node.condition),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, cond_node.id)
        
        # Create loop exit node
        exit_node = self.graph.add_node('loop_exit', {'label': 'loop_exit'})
        
        # Set up break/continue targets
        self.break_targets.append(exit_node.id)
        self.continue_targets.append(cond_node.id)
        
        # Create loop body
        body_entry = cond_node.id
        for stmt in node.body:
            body_entry = self.visit(stmt, body_entry)
        
        # Loop back to condition
        self.graph.add_edge(body_entry, cond_node.id, 'loop_back')
        
        # Exit when condition false
        self.graph.add_edge(cond_node.id, exit_node.id, 'exit')
        
        # Pop break/continue targets
        self.break_targets.pop()
        self.continue_targets.pop()
        
        return exit_node.id
    
    def visit_for(self, node: ForLoopNode, from_node_id: int) -> int:
        """Create for-each loop structure"""
        # Create iterator setup node
        iter_node = self.graph.add_node('for_setup', {
            'iterator': node.iterator_var,
            'iterable': self.serialize_expression(node.iterable),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, iter_node.id)
        
        # Create loop condition node (has next element)
        cond_node = self.graph.add_node('for_condition', {
            'iterator': node.iterator_var
        })
        self.graph.add_edge(iter_node.id, cond_node.id)
        
        # Create loop exit node
        exit_node = self.graph.add_node('loop_exit', {'label': 'loop_exit'})
        
        # Set up break/continue targets
        self.break_targets.append(exit_node.id)
        self.continue_targets.append(cond_node.id)
        
        # Create loop body
        body_entry = cond_node.id
        for stmt in node.body:
            body_entry = self.visit(stmt, body_entry)
        
        # Loop back to condition
        self.graph.add_edge(body_entry, cond_node.id, 'loop_back')
        
        # Exit when no more elements
        self.graph.add_edge(cond_node.id, exit_node.id, 'exit')
        
        # Pop break/continue targets
        self.break_targets.pop()
        self.continue_targets.pop()
        
        return exit_node.id
    
    def visit_repeat(self, node: RepeatLoopNode, from_node_id: int) -> int:
        """Create repeat N times loop"""
        # Create counter initialization
        counter_node = self.graph.add_node('repeat_setup', {
            'count': self.serialize_expression(node.count),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, counter_node.id)
        
        # Create condition node
        cond_node = self.graph.add_node('repeat_condition', {
            'count': self.serialize_expression(node.count)
        })
        self.graph.add_edge(counter_node.id, cond_node.id)
        
        # Create loop exit node
        exit_node = self.graph.add_node('loop_exit', {'label': 'loop_exit'})
        
        # Set up break/continue targets
        self.break_targets.append(exit_node.id)
        self.continue_targets.append(cond_node.id)
        
        # Create loop body
        body_entry = cond_node.id
        for stmt in node.body:
            body_entry = self.visit(stmt, body_entry)
        
        # Loop back to condition
        self.graph.add_edge(body_entry, cond_node.id, 'loop_back')
        
        # Exit when count reached
        self.graph.add_edge(cond_node.id, exit_node.id, 'exit')
        
        # Pop break/continue targets
        self.break_targets.pop()
        self.continue_targets.pop()
        
        return exit_node.id
    
    def visit_function_def(self, node: FunctionDefNode, from_node_id: int) -> int:
        """Create function definition node"""
        # For now, store function definition as a node
        # In full implementation, would create separate graph for function body
        func_node = self.graph.add_node('function_def', {
            'name': node.name,
            'parameters': node.parameters,
            'body': [self.serialize_statement(stmt) for stmt in node.body],
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, func_node.id)
        return func_node.id

    def serialize_statement(self, stmt: ASTNode) -> Dict:
        """Serialize a statement AST node into a JSON-safe dict."""
        if stmt is None:
            return {'type': 'noop'}

        if isinstance(stmt, AssignmentNode):
            return {
                'type': 'assignment',
                'variable': stmt.variable_name,
                'value': self.serialize_expression(stmt.value),
                'line': stmt.line_number
            }

        if isinstance(stmt, OutputNode):
            return {
                'type': 'output',
                'expressions': [self.serialize_expression(e) for e in stmt.expressions],
                'newline': stmt.newline,
                'line': stmt.line_number
            }

        if isinstance(stmt, InputNode):
            return {
                'type': 'input',
                'prompt': stmt.prompt,
                'variable': stmt.variable_name,
                'input_type': stmt.input_type,
                'line': stmt.line_number
            }

        if isinstance(stmt, IfStatementNode):
            return {
                'type': 'if',
                'condition': self.serialize_expression(stmt.condition),
                'then': [self.serialize_statement(s) for s in stmt.then_block],
                'else': [self.serialize_statement(s) for s in stmt.else_block],
                'line': stmt.line_number
            }

        if isinstance(stmt, WhileLoopNode):
            return {
                'type': 'while',
                'condition': self.serialize_expression(stmt.condition),
                'body': [self.serialize_statement(s) for s in stmt.body],
                'line': stmt.line_number
            }

        if isinstance(stmt, ForLoopNode):
            return {
                'type': 'for_each',
                'iterator': stmt.iterator_var,
                'iterable': self.serialize_expression(stmt.iterable),
                'body': [self.serialize_statement(s) for s in stmt.body],
                'line': stmt.line_number
            }

        if isinstance(stmt, RepeatLoopNode):
            return {
                'type': 'repeat',
                'count': self.serialize_expression(stmt.count),
                'body': [self.serialize_statement(s) for s in stmt.body],
                'line': stmt.line_number
            }

        if isinstance(stmt, FunctionCallNode):
            return {
                'type': 'function_call',
                'function': stmt.function_name,
                'arguments': [self.serialize_expression(a) for a in stmt.arguments],
                'line': stmt.line_number
            }

        if isinstance(stmt, ReturnNode):
            return {
                'type': 'return',
                'value': self.serialize_expression(stmt.value) if stmt.value else None,
                'line': stmt.line_number
            }

        if isinstance(stmt, BreakNode):
            return {'type': 'break', 'line': stmt.line_number}

        if isinstance(stmt, ContinueNode):
            return {'type': 'continue', 'line': stmt.line_number}

        if isinstance(stmt, ListAppendNode):
            return {
                'type': 'list_append',
                'list': self.serialize_expression(stmt.list_var),
                'value': self.serialize_expression(stmt.value),
                'line': stmt.line_number
            }

        if isinstance(stmt, FileReadNode):
            return {
                'type': 'file_read',
                'filepath': self.serialize_expression(stmt.filepath),
                'variable': stmt.variable_name,
                'mode': stmt.mode,
                'line': stmt.line_number
            }

        if isinstance(stmt, FileWriteNode):
            return {
                'type': 'file_write',
                'filepath': self.serialize_expression(stmt.filepath),
                'content': self.serialize_expression(stmt.content),
                'mode': stmt.mode,
                'line': stmt.line_number
            }

        # Fallback: treat as expression statement
        return {
            'type': 'expr',
            'expr': self.serialize_expression(stmt),
            'line': getattr(stmt, 'line_number', 0)
        }
    
    def visit_function_call(self, node: FunctionCallNode, from_node_id: int) -> int:
        """Create function call node"""
        call_node = self.graph.add_node('function_call', {
            'function': node.function_name,
            'arguments': [self.serialize_expression(arg) for arg in node.arguments],
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, call_node.id)
        return call_node.id
    
    def visit_return(self, node: ReturnNode, from_node_id: int) -> int:
        """Create return node"""
        return_node = self.graph.add_node('return', {
            'value': self.serialize_expression(node.value) if node.value else None,
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, return_node.id)
        return return_node.id
    
    def visit_break(self, node: BreakNode, from_node_id: int) -> int:
        """Create break node"""
        break_node = self.graph.add_node('break', {'line': node.line_number})
        self.graph.add_edge(from_node_id, break_node.id)
        
        # Connect to loop exit if in loop
        if self.break_targets:
            self.graph.add_edge(break_node.id, self.break_targets[-1], 'break_to')
        
        return break_node.id
    
    def visit_continue(self, node: ContinueNode, from_node_id: int) -> int:
        """Create continue node"""
        continue_node = self.graph.add_node('continue', {'line': node.line_number})
        self.graph.add_edge(from_node_id, continue_node.id)
        
        # Connect to loop condition if in loop
        if self.continue_targets:
            self.graph.add_edge(continue_node.id, self.continue_targets[-1], 'continue_to')
        
        return continue_node.id
    
    def visit_file_read(self, node: FileReadNode, from_node_id: int) -> int:
        """Create file read node"""
        read_node = self.graph.add_node('file_read', {
            'filepath': self.serialize_expression(node.filepath),
            'variable': node.variable_name,
            'mode': node.mode,
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, read_node.id)
        return read_node.id
    
    def visit_file_write(self, node: FileWriteNode, from_node_id: int) -> int:
        """Create file write node"""
        write_node = self.graph.add_node('file_write', {
            'filepath': self.serialize_expression(node.filepath),
            'content': self.serialize_expression(node.content),
            'mode': node.mode,
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, write_node.id)
        return write_node.id
    
    def visit_list_append(self, node: ListAppendNode, from_node_id: int) -> int:
        """Create list append node"""
        append_node = self.graph.add_node('list_append', {
            'list': self.serialize_expression(node.list_var),
            'value': self.serialize_expression(node.value),
            'line': node.line_number
        })
        self.graph.add_edge(from_node_id, append_node.id)
        return append_node.id
    
    def serialize_expression(self, expr: ASTNode) -> Dict:
        """Convert expression AST node to serializable dict"""
        if expr is None:
            return None
        
        if isinstance(expr, LiteralNode):
            # Handle list literals specially
            if expr.node_type == NodeType.LIST and isinstance(expr.value, list):
                return {
                    'type': 'list_literal',
                    'elements': [self.serialize_expression(e) for e in expr.value]
                }
            return {
                'type': 'literal',
                'value': expr.value,
                'value_type': expr.node_type.value
            }
        
        elif isinstance(expr, VariableNode):
            return {
                'type': 'variable',
                'name': expr.name
            }
        
        elif isinstance(expr, BinaryOpNode):
            return {
                'type': 'binary_op',
                'operator': expr.operator,
                'left': self.serialize_expression(expr.left),
                'right': self.serialize_expression(expr.right)
            }
        
        elif isinstance(expr, ComparisonNode):
            return {
                'type': 'comparison',
                'operator': expr.operator,
                'left': self.serialize_expression(expr.left),
                'right': self.serialize_expression(expr.right)
            }
        
        elif isinstance(expr, LogicalOpNode):
            return {
                'type': 'logical_op',
                'operator': expr.operator,
                'operands': [self.serialize_expression(op) for op in expr.operands]
            }
        
        elif isinstance(expr, FunctionCallNode):
            return {
                'type': 'function_call',
                'function': expr.function_name,
                'arguments': [self.serialize_expression(arg) for arg in expr.arguments]
            }
        
        return {'type': 'unknown', 'repr': repr(expr)}
