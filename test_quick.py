"""
Quick test script to verify IntentLang installation
"""

import sys
from intentlang.parser import IntentParser
from intentlang.logic_graph import LogicGraph
from intentlang.interpreter import IntentInterpreter


def test_basic():
    """Test basic functionality"""
    print("🧪 Testing IntentLang Basic Functionality\n")
    
    # Test 1: Simple output
    print("Test 1: Simple Output")
    code = 'Display "Hello, IntentLang!".'
    
    parser = IntentParser()
    ast = parser.parse(code)
    
    if parser.errors:
        print(f"❌ Parser errors: {parser.errors}")
        return False
    
    graph = LogicGraph()
    graph.from_ast(ast)
    
    interpreter = IntentInterpreter()
    print("Output: ", end="")
    interpreter.execute(graph)
    print("✅ Test 1 passed\n")
    
    # Test 2: Variables and arithmetic
    print("Test 2: Variables and Arithmetic")
    code = """
Set x to 5.
Set y to 10.
Add x and y and store the result in sum.
Display "The sum is: " followed by the value of sum.
    """
    
    ast = parser.parse(code)
    if parser.errors:
        print(f"❌ Parser errors: {parser.errors}")
        return False
    
    graph = LogicGraph()
    graph.from_ast(ast)
    
    interpreter = IntentInterpreter()
    print("Output: ", end="")
    interpreter.execute(graph)
    print("✅ Test 2 passed\n")
    
    # Test 3: Conditionals
    print("Test 3: Conditionals")
    code = """
Set age to 25.
If age is greater than or equal to 18:
  Display "Adult".
Otherwise:
  Display "Minor".
    """
    
    ast = parser.parse(code)
    if parser.errors:
        print(f"❌ Parser errors: {parser.errors}")
        return False
    
    graph = LogicGraph()
    graph.from_ast(ast)
    
    interpreter = IntentInterpreter()
    print("Output: ", end="")
    interpreter.execute(graph)
    print("✅ Test 3 passed\n")
    
    # Test 4: Loops
    print("Test 4: Loops")
    code = """
Set counter to 0.
Repeat 3 times:
  Increment counter.
Display "Counter: " followed by the value of counter.
    """
    
    ast = parser.parse(code)
    if parser.errors:
        print(f"❌ Parser errors: {parser.errors}")
        return False
    
    graph = LogicGraph()
    graph.from_ast(ast)
    
    interpreter = IntentInterpreter()
    print("Output: ", end="")
    interpreter.execute(graph)
    print("✅ Test 4 passed\n")
    
    # Test 5: Lists
    print("Test 5: Lists")
    code = """
Create a list called numbers with values [1, 2, 3].
Display "Numbers: " followed by the value of numbers.
    """
    
    ast = parser.parse(code)
    if parser.errors:
        print(f"❌ Parser errors: {parser.errors}")
        return False
    
    graph = LogicGraph()
    graph.from_ast(ast)
    
    interpreter = IntentInterpreter()
    print("Output: ", end="")
    interpreter.execute(graph)
    print("✅ Test 5 passed\n")
    
    print("="*50)
    print("🎉 All tests passed! IntentLang is working!")
    print("="*50)
    return True


if __name__ == '__main__':
    try:
        success = test_basic()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
