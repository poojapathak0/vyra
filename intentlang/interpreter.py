"""
IntentLang Interpreter - Executes logic graphs
Traverses the graph and executes operations with proper state management
"""

import sys
import json
from typing import Any, Dict, List, Optional
from .logic_graph import LogicGraph, GraphNode


class ExecutionContext:
    """Manages variable scopes and execution state"""
    
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes (global at bottom)
        self.functions = {}  # Function definitions
        self.return_value = None
        self.should_return = False
        self.should_break = False
        self.should_continue = False
    
    def push_scope(self):
        """Enter a new scope (function call, block)"""
        self.scopes.append({})
    
    def pop_scope(self):
        """Exit current scope"""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def get_variable(self, name: str) -> Any:
        """Get variable value from current or parent scopes"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' is not defined")
    
    def set_variable(self, name: str, value: Any):
        """Set variable in current scope"""
        self.scopes[-1][name] = value
    
    def has_variable(self, name: str) -> bool:
        """Check if variable exists in any scope"""
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False
    
    def define_function(self, name: str, params: List[str], body_data: Any):
        """Register a function"""
        self.functions[name] = {
            'params': params,
            'body': body_data
        }
    
    def get_function(self, name: str) -> Dict:
        """Get function definition"""
        if name in self.functions:
            return self.functions[name]
        raise NameError(f"Function '{name}' is not defined")


class IntentInterpreter:
    """
    Interpreter for IntentLang logic graphs
    Executes programs by traversing the graph and maintaining execution state
    """
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.context = ExecutionContext()
        self.max_iterations = 100000  # Prevent infinite loops
        self.iteration_count = 0
    
    def execute(self, graph: LogicGraph) -> Any:
        """Execute a logic graph"""
        self.context = ExecutionContext()
        self.iteration_count = 0
        
        if graph.entry_node_id is None:
            raise RuntimeError("Graph has no entry node")
        
        # Start execution from entry node
        return self._execute_from_node(graph, graph.entry_node_id)
    
    def _execute_from_node(self, graph: LogicGraph, node_id: int) -> Any:
        """Execute graph starting from given node"""
        current_id = node_id
        
        while current_id is not None:
            self.iteration_count += 1
            
            # Safety check for infinite loops
            if self.iteration_count > self.max_iterations:
                raise RuntimeError(f"Exceeded maximum iterations ({self.max_iterations}). Possible infinite loop.")
            
            # Get current node
            if current_id not in graph.nodes:
                break
            
            node = graph.nodes[current_id]
            
            if self.debug:
                print(f"[DEBUG] Executing node {node.id}: {node.type}")
            
            # Execute node
            next_id = self._execute_node(graph, node)
            
            # Handle control flow
            if self.context.should_return:
                return self.context.return_value
            
            if self.context.should_break:
                # Find break target
                break
            
            if self.context.should_continue:
                # Find continue target
                self.context.should_continue = False
            
            current_id = next_id
        
        return None
    
    def _execute_node(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute a single node and return next node ID"""
        
        if node.type == 'entry':
            return self._get_next_node(graph, node)
        
        elif node.type == 'exit':
            return None
        
        elif node.type == 'assignment':
            return self._execute_assignment(graph, node)
        
        elif node.type == 'output':
            return self._execute_output(graph, node)
        
        elif node.type == 'input':
            return self._execute_input(graph, node)
        
        elif node.type == 'if':
            return self._execute_if(graph, node)
        
        elif node.type == 'while':
            return self._execute_while(graph, node)
        
        elif node.type == 'for_setup':
            return self._execute_for_setup(graph, node)
        
        elif node.type == 'for_condition':
            return self._execute_for_condition(graph, node)
        
        elif node.type == 'repeat_setup':
            return self._execute_repeat_setup(graph, node)
        
        elif node.type == 'repeat_condition':
            return self._execute_repeat_condition(graph, node)
        
        elif node.type == 'function_def':
            return self._execute_function_def(graph, node)
        
        elif node.type == 'function_call':
            return self._execute_function_call(graph, node)
        
        elif node.type == 'return':
            return self._execute_return(graph, node)
        
        elif node.type == 'break':
            self.context.should_break = True
            return self._find_break_target(graph, node)
        
        elif node.type == 'continue':
            self.context.should_continue = True
            return self._find_continue_target(graph, node)
        
        elif node.type == 'merge':
            return self._get_next_node(graph, node)
        
        elif node.type == 'loop_exit':
            return self._get_next_node(graph, node)
        
        elif node.type == 'file_read':
            return self._execute_file_read(graph, node)
        
        elif node.type == 'file_write':
            return self._execute_file_write(graph, node)
        
        elif node.type == 'list_append':
            return self._execute_list_append(graph, node)
        
        else:
            if self.debug:
                print(f"[DEBUG] Unknown node type: {node.type}")
            return self._get_next_node(graph, node)
    
    def _execute_assignment(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute variable assignment"""
        var_name = node.data['variable']
        value_expr = node.data['value']
        
        value = self._evaluate_expression(value_expr)
        self.context.set_variable(var_name, value)
        
        if self.debug:
            print(f"[DEBUG] Assigned {var_name} = {value}")
        
        return self._get_next_node(graph, node)
    
    def _execute_output(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute output/print"""
        expressions = node.data['expressions']
        outputs = []
        
        for expr in expressions:
            value = self._evaluate_expression(expr)
            outputs.append(str(value))
        
        output_text = ''.join(outputs)
        
        if node.data.get('newline', True):
            print(output_text)
        else:
            print(output_text, end='')
        
        return self._get_next_node(graph, node)
    
    def _execute_input(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute user input"""
        prompt = node.data['prompt']
        var_name = node.data['variable']
        input_type = node.data.get('input_type', 'string')
        
        if input_type == 'password':
            import getpass
            value = getpass.getpass(prompt)
        else:
            value = input(prompt)
        
        # Try to convert to number if it looks like one
        if input_type == 'number' or (value.replace('.', '').replace('-', '').isdigit()):
            try:
                value = float(value) if '.' in value else int(value)
            except ValueError:
                pass
        
        self.context.set_variable(var_name, value)
        
        if self.debug:
            print(f"[DEBUG] Input stored in {var_name}: {value}")
        
        return self._get_next_node(graph, node)
    
    def _execute_if(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute if statement"""
        condition_expr = node.data['condition']
        condition_value = self._evaluate_expression(condition_expr)
        
        if self.debug:
            print(f"[DEBUG] If condition: {condition_value}")
        
        # Find then and else branches
        successors = node.successors
        
        if self._is_truthy(condition_value):
            # Execute then branch - find first non-merge successor
            for succ_id in successors:
                succ_node = graph.nodes[succ_id]
                if succ_node.type != 'merge':
                    return succ_id
        else:
            # Execute else branch or skip to merge
            for succ_id in successors:
                succ_node = graph.nodes[succ_id]
                if succ_node.type == 'merge':
                    return succ_id
        
        return self._get_next_node(graph, node)
    
    def _execute_while(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute while loop condition check"""
        condition_expr = node.data['condition']
        condition_value = self._evaluate_expression(condition_expr)
        
        if self.debug:
            print(f"[DEBUG] While condition: {condition_value}")
        
        if self._is_truthy(condition_value):
            # Enter loop body
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') != 'exit':
                    return succ_id
        else:
            # Exit loop
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'exit':
                    return succ_id
        
        return self._get_next_node(graph, node)
    
    def _execute_for_setup(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Set up for-each loop"""
        iterator_var = node.data['iterator']
        iterable_expr = node.data['iterable']
        
        iterable = self._evaluate_expression(iterable_expr)
        
        # Store iterator info in context
        self.context.set_variable(f'__iter_{iterator_var}', iter(iterable))
        self.context.set_variable(f'__iter_{iterator_var}_var', iterator_var)
        
        return self._get_next_node(graph, node)
    
    def _execute_for_condition(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Check for-each loop condition"""
        iterator_var = node.data['iterator']
        iterator = self.context.get_variable(f'__iter_{iterator_var}')
        
        try:
            next_value = next(iterator)
            self.context.set_variable(iterator_var, next_value)
            
            # Enter loop body
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') != 'exit':
                    return succ_id
        except StopIteration:
            # Exit loop
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'exit':
                    return succ_id
        
        return self._get_next_node(graph, node)
    
    def _execute_repeat_setup(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Set up repeat N times loop"""
        count_expr = node.data['count']
        count = self._evaluate_expression(count_expr)
        
        # Store counter
        self.context.set_variable('__repeat_counter', 0)
        self.context.set_variable('__repeat_max', int(count))
        
        return self._get_next_node(graph, node)
    
    def _execute_repeat_condition(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Check repeat loop condition"""
        counter = self.context.get_variable('__repeat_counter')
        max_count = self.context.get_variable('__repeat_max')
        
        if counter < max_count:
            # Increment counter
            self.context.set_variable('__repeat_counter', counter + 1)
            
            # Enter loop body
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') != 'exit':
                    return succ_id
        else:
            # Exit loop
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'exit':
                    return succ_id
        
        return self._get_next_node(graph, node)
    
    def _execute_function_def(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Register function definition"""
        name = node.data['name']
        params = node.data['parameters']
        body = node.data['body']
        
        self.context.define_function(name, params, body)
        
        if self.debug:
            print(f"[DEBUG] Defined function {name} with params {params}")
        
        return self._get_next_node(graph, node)
    
    def _execute_function_call(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute function call"""
        func_name = node.data['function']
        args = node.data['arguments']
        
        # Evaluate arguments
        arg_values = [self._evaluate_expression(arg) for arg in args]
        
        # Get function definition
        func = self.context.get_function(func_name)
        
        # Create new scope for function
        self.context.push_scope()
        
        # Bind parameters
        for param, value in zip(func['params'], arg_values):
            self.context.set_variable(param, value)
        
        # Execute function body (simplified - would need separate graph traversal)
        # For now, just pop scope
        self.context.pop_scope()
        
        if self.debug:
            print(f"[DEBUG] Called function {func_name} with {arg_values}")
        
        return self._get_next_node(graph, node)
    
    def _execute_return(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute return statement"""
        value_expr = node.data.get('value')
        
        if value_expr:
            self.context.return_value = self._evaluate_expression(value_expr)
        else:
            self.context.return_value = None
        
        self.context.should_return = True
        
        if self.debug:
            print(f"[DEBUG] Returning: {self.context.return_value}")
        
        return None
    
    def _execute_file_read(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute file read"""
        filepath_expr = node.data['filepath']
        var_name = node.data['variable']
        mode = node.data.get('mode', 'text')
        
        filepath = self._evaluate_expression(filepath_expr)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            if mode == 'json':
                content = json.loads(content)
            
            self.context.set_variable(var_name, content)
            
            if self.debug:
                print(f"[DEBUG] Read file {filepath} into {var_name}")
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
        
        return self._get_next_node(graph, node)
    
    def _execute_file_write(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute file write"""
        filepath_expr = node.data['filepath']
        content_expr = node.data['content']
        mode = node.data.get('mode', 'text')
        
        filepath = self._evaluate_expression(filepath_expr)
        content = self._evaluate_expression(content_expr)
        
        try:
            with open(filepath, 'w') as f:
                if mode == 'json':
                    json.dump(content, f, indent=2)
                else:
                    f.write(str(content))
            
            if self.debug:
                print(f"[DEBUG] Wrote to file {filepath}")
        except Exception as e:
            print(f"Error writing file {filepath}: {e}")
        
        return self._get_next_node(graph, node)
    
    def _execute_list_append(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Execute list append"""
        list_expr = node.data['list']
        value_expr = node.data['value']
        
        # Get list variable name
        if list_expr['type'] == 'variable':
            list_var = list_expr['name']
            lst = self.context.get_variable(list_var)
            value = self._evaluate_expression(value_expr)
            
            if not isinstance(lst, list):
                lst = []
                self.context.set_variable(list_var, lst)
            
            lst.append(value)
            
            if self.debug:
                print(f"[DEBUG] Appended {value} to {list_var}")
        
        return self._get_next_node(graph, node)
    
    def _evaluate_expression(self, expr: Dict) -> Any:
        """Evaluate an expression dictionary"""
        if expr is None:
            return None
        
        expr_type = expr.get('type')
        
        if expr_type == 'literal':
            return expr['value']
        
        elif expr_type == 'list_literal':
            return [self._evaluate_expression(e) for e in expr['elements']]
        
        elif expr_type == 'variable':
            return self.context.get_variable(expr['name'])
        
        elif expr_type == 'binary_op':
            left = self._evaluate_expression(expr['left'])
            right = self._evaluate_expression(expr['right'])
            op = expr['operator']
            
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right if right != 0 else float('inf')
            elif op == '%':
                return left % right if right != 0 else 0
            elif op == '**':
                return left ** right
        
        elif expr_type == 'comparison':
            left = self._evaluate_expression(expr['left'])
            right = self._evaluate_expression(expr['right'])
            op = expr['operator']
            
            if op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
            elif op == '<=':
                return left <= right
            elif op == '>=':
                return left >= right
        
        elif expr_type == 'logical_op':
            op = expr['operator']
            operands = expr['operands']
            
            if op == 'and':
                result = True
                for operand in operands:
                    result = result and self._is_truthy(self._evaluate_expression(operand))
                return result
            elif op == 'or':
                result = False
                for operand in operands:
                    result = result or self._is_truthy(self._evaluate_expression(operand))
                return result
            elif op == 'not':
                return not self._is_truthy(self._evaluate_expression(operands[0]))
        
        elif expr_type == 'function_call':
            # Handle built-in functions
            func_name = expr['function']
            args = [self._evaluate_expression(arg) for arg in expr['arguments']]
            return self._call_builtin(func_name, args)
        
        return None
    
    def _call_builtin(self, name: str, args: List[Any]) -> Any:
        """Call built-in function"""
        if name == 'len' or name == 'length':
            return len(args[0]) if args else 0
        elif name == 'str':
            return str(args[0]) if args else ""
        elif name == 'int':
            return int(args[0]) if args else 0
        elif name == 'float':
            return float(args[0]) if args else 0.0
        elif name == 'abs':
            return abs(args[0]) if args else 0
        elif name == 'round':
            return round(args[0]) if args else 0
        # Add more built-ins as needed
        return None
    
    def _is_truthy(self, value: Any) -> bool:
        """Check if value is truthy"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value.lower() not in ['false', 'no', '', '0']
        if value is None:
            return False
        return bool(value)
    
    def _get_next_node(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Get next node in linear flow"""
        if node.successors:
            return node.successors[0]
        return None
    
    def _find_break_target(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Find loop exit node for break"""
        # Look for edges with 'break_to' type
        for succ_id in node.successors:
            return succ_id
        return None
    
    def _find_continue_target(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Find loop condition node for continue"""
        # Look for edges with 'continue_to' type
        for succ_id in node.successors:
            return succ_id
        return None
