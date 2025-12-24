"""
IntentLang Interpreter - Executes logic graphs
Traverses the graph and executes operations with proper state management
"""

import sys
import json
import math
import random
import time
from datetime import datetime
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
        self.max_call_depth = 200
        self.call_depth = 0
    
    def execute(self, graph: LogicGraph) -> Any:
        """Execute a logic graph"""
        self.context = ExecutionContext()
        self.iteration_count = 0
        self.call_depth = 0
        
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
            return self._find_break_target(graph, node)
        
        elif node.type == 'continue':
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
        
        truthy = self._is_truthy(condition_value)

        # Follow explicit edge labels when present
        if truthy:
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'then':
                    return succ_id
        else:
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'else':
                    return succ_id
            for succ_id in node.successors:
                edge = graph.graph[node.id][succ_id]
                if edge.get('type') == 'else_skip':
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

        # Statement-form call: execute and ignore return value
        self._call_function(func_name, arg_values)

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
            func_name = expr['function']
            args = [self._evaluate_expression(arg) for arg in expr['arguments']]
            return self._call_function(func_name, args)
        
        return None
    
    def _call_builtin(self, name: str, args: List[Any]) -> Any:
        """Call built-in function"""
        n = (name or '').strip().lower()

        # Type / basics
        if n in ['len', 'length']:
            return len(args[0]) if args else 0
        if n in ['str', 'to_string', 'string']:
            return str(args[0]) if args else ""
        if n in ['int', 'to_int']:
            return int(args[0]) if args else 0
        if n in ['float', 'to_float']:
            return float(args[0]) if args else 0.0
        if n == 'type_of':
            return type(args[0]).__name__ if args else 'none'

        # Math
        if n == 'abs':
            return abs(args[0]) if args else 0
        if n == 'round':
            return round(args[0]) if args else 0
        if n == 'floor':
            return math.floor(args[0]) if args else 0
        if n == 'ceil':
            return math.ceil(args[0]) if args else 0
        if n == 'sqrt':
            return math.sqrt(args[0]) if args else 0
        if n == 'sin':
            return math.sin(args[0]) if args else 0
        if n == 'cos':
            return math.cos(args[0]) if args else 0
        if n == 'tan':
            return math.tan(args[0]) if args else 0
        if n == 'log':
            return math.log(args[0]) if args else 0
        if n == 'exp':
            return math.exp(args[0]) if args else 0

        # String
        if n in ['uppercase', 'upper']:
            return str(args[0]).upper() if args else ""
        if n in ['lowercase', 'lower']:
            return str(args[0]).lower() if args else ""
        if n == 'substring':
            s = str(args[0]) if args else ""
            start = int(args[1]) if len(args) > 1 else 0
            end = int(args[2]) if len(args) > 2 else None
            return s[start:end]
        if n == 'split':
            s = str(args[0]) if args else ""
            sep = str(args[1]) if len(args) > 1 else None
            return s.split(sep)
        if n == 'join':
            sep = str(args[0]) if args else ""
            items = args[1] if len(args) > 1 else []
            return sep.join([str(x) for x in items])
        if n == 'replace':
            s = str(args[0]) if args else ""
            old = str(args[1]) if len(args) > 1 else ""
            new = str(args[2]) if len(args) > 2 else ""
            return s.replace(old, new)

        # List / collections
        if n == 'append':
            lst = args[0] if args else []
            val = args[1] if len(args) > 1 else None
            if isinstance(lst, list):
                lst.append(val)
            return lst
        if n == 'remove':
            lst = args[0] if args else []
            val = args[1] if len(args) > 1 else None
            if isinstance(lst, list) and val in lst:
                lst.remove(val)
            return lst
        if n == 'sort':
            lst = args[0] if args else []
            if isinstance(lst, list):
                lst.sort()
            return lst

        # Time
        if n == 'current_time':
            return datetime.now().isoformat()
        if n == 'timestamp':
            return time.time()
        if n == 'sleep':
            seconds = float(args[0]) if args else 0.0
            time.sleep(max(0.0, seconds))
            return None

        # Random
        if n == 'random_number':
            if len(args) >= 2:
                return random.uniform(float(args[0]), float(args[1]))
            return random.random()
        if n == 'random_choice':
            seq = args[0] if args else []
            return random.choice(seq) if seq else None
        if n == 'shuffle':
            seq = args[0] if args else []
            if isinstance(seq, list):
                random.shuffle(seq)
            return seq

        return None

    def _call_function(self, name: str, args: List[Any]) -> Any:
        """Call either a built-in or a user-defined function."""
        # Prefer built-ins when available
        builtin_result = self._call_builtin(name, args)
        if builtin_result is not None or (name or '').strip().lower() in {
            'sleep', 'append', 'remove', 'sort', 'shuffle'
        }:
            return builtin_result

        if name not in self.context.functions:
            raise NameError(f"Function '{name}' is not defined")

        if self.call_depth >= self.max_call_depth:
            raise RuntimeError(f"Exceeded maximum call depth ({self.max_call_depth}).")

        func = self.context.get_function(name)
        params = func.get('params', [])
        body = func.get('body', [])

        self.call_depth += 1
        self.context.push_scope()
        try:
            for param, value in zip(params, args):
                self.context.set_variable(param, value)

            status, value = self._execute_serialized_statements(body)
            if status == 'return':
                return value
            return None
        finally:
            self.context.pop_scope()
            self.call_depth -= 1

    def _execute_serialized_statements(self, statements: List[Dict]) -> tuple[str, Any]:
        """Execute a list of serialized statements.

        Returns (status, value) where status is one of: 'ok', 'return', 'break', 'continue'.
        """
        for stmt in statements or []:
            status, value = self._execute_serialized_statement(stmt)
            if status != 'ok':
                return status, value
        return 'ok', None

    def _execute_serialized_statement(self, stmt: Dict) -> tuple[str, Any]:
        t = (stmt or {}).get('type')

        if t == 'noop' or t is None:
            return 'ok', None

        if t == 'assignment':
            var_name = stmt['variable']
            value = self._evaluate_expression(stmt.get('value'))
            self.context.set_variable(var_name, value)
            return 'ok', None

        if t == 'output':
            outputs = []
            for expr in stmt.get('expressions', []):
                outputs.append(str(self._evaluate_expression(expr)))
            text = ''.join(outputs)
            if stmt.get('newline', True):
                print(text)
            else:
                print(text, end='')
            return 'ok', None

        if t == 'input':
            prompt = stmt.get('prompt', '')
            var = stmt.get('variable')
            input_type = stmt.get('input_type', 'string')
            if input_type == 'password':
                import getpass
                value = getpass.getpass(prompt)
            else:
                value = input(prompt)
            if input_type == 'number' or (isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit()):
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    pass
            if var:
                self.context.set_variable(var, value)
            return 'ok', None

        if t == 'function_call':
            func_name = stmt.get('function')
            args = [self._evaluate_expression(a) for a in stmt.get('arguments', [])]
            self._call_function(func_name, args)
            return 'ok', None

        if t == 'return':
            value_expr = stmt.get('value')
            value = self._evaluate_expression(value_expr) if value_expr is not None else None
            return 'return', value

        if t == 'break':
            return 'break', None

        if t == 'continue':
            return 'continue', None

        if t == 'list_append':
            list_expr = stmt.get('list')
            value_expr = stmt.get('value')
            if list_expr and list_expr.get('type') == 'variable':
                list_var = list_expr.get('name')
                lst = self.context.get_variable(list_var)
                value = self._evaluate_expression(value_expr)
                if not isinstance(lst, list):
                    lst = []
                    self.context.set_variable(list_var, lst)
                lst.append(value)
            return 'ok', None

        if t == 'file_read':
            filepath = self._evaluate_expression(stmt.get('filepath'))
            var_name = stmt.get('variable')
            mode = stmt.get('mode', 'text')
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                if mode == 'json':
                    content = json.loads(content)
                if var_name:
                    self.context.set_variable(var_name, content)
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
            return 'ok', None

        if t == 'file_write':
            filepath = self._evaluate_expression(stmt.get('filepath'))
            content = self._evaluate_expression(stmt.get('content'))
            mode = stmt.get('mode', 'text')
            try:
                with open(filepath, 'w') as f:
                    if mode == 'json':
                        json.dump(content, f, indent=2)
                    else:
                        f.write(str(content))
            except Exception as e:
                print(f"Error writing file {filepath}: {e}")
            return 'ok', None

        if t == 'if':
            cond = self._evaluate_expression(stmt.get('condition'))
            branch = stmt.get('then', []) if self._is_truthy(cond) else stmt.get('else', [])
            return self._execute_serialized_statements(branch)

        if t == 'while':
            while self._is_truthy(self._evaluate_expression(stmt.get('condition'))):
                self.iteration_count += 1
                if self.iteration_count > self.max_iterations:
                    raise RuntimeError(f"Exceeded maximum iterations ({self.max_iterations}). Possible infinite loop.")
                status, value = self._execute_serialized_statements(stmt.get('body', []))
                if status == 'return':
                    return status, value
                if status == 'break':
                    break
                if status == 'continue':
                    continue
            return 'ok', None

        if t == 'repeat':
            count = int(self._evaluate_expression(stmt.get('count')) or 0)
            for _ in range(max(0, count)):
                self.iteration_count += 1
                if self.iteration_count > self.max_iterations:
                    raise RuntimeError(f"Exceeded maximum iterations ({self.max_iterations}). Possible infinite loop.")
                status, value = self._execute_serialized_statements(stmt.get('body', []))
                if status == 'return':
                    return status, value
                if status == 'break':
                    break
                if status == 'continue':
                    continue
            return 'ok', None

        if t == 'for_each':
            iterator_name = stmt.get('iterator')
            iterable = self._evaluate_expression(stmt.get('iterable'))
            for item in (iterable or []):
                self.iteration_count += 1
                if self.iteration_count > self.max_iterations:
                    raise RuntimeError(f"Exceeded maximum iterations ({self.max_iterations}). Possible infinite loop.")
                self.context.set_variable(iterator_name, item)
                status, value = self._execute_serialized_statements(stmt.get('body', []))
                if status == 'return':
                    return status, value
                if status == 'break':
                    break
                if status == 'continue':
                    continue
            return 'ok', None

        # Unknown statement type
        return 'ok', None
    
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
        for succ_id in node.successors:
            edge = graph.graph[node.id][succ_id]
            if edge.get('type') == 'break_to':
                return succ_id
        if node.successors:
            return node.successors[0]
        return None
    
    def _find_continue_target(self, graph: LogicGraph, node: GraphNode) -> Optional[int]:
        """Find loop condition node for continue"""
        for succ_id in node.successors:
            edge = graph.graph[node.id][succ_id]
            if edge.get('type') == 'continue_to':
                return succ_id
        if node.successors:
            return node.successors[0]
        return None
