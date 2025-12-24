# Vyra Language Specification v1.0

## Overview

Vyra is a natural language programming language that allows developers to write code using plain English sentences. This document defines the formal grammar, semantics, and execution model.

## Design Principles

1. **Natural Language First**: Code reads like instructions to a human
2. **Deterministic Execution**: No ambiguity—same input always produces same output
3. **Type Inference**: Types are inferred from context and usage
4. **Explicit Intent**: Actions are clearly stated with verbs
5. **Progressive Disclosure**: Simple things are simple, complex things are possible

## Grammar

### Sentence Structure

Every statement in Vyra follows patterns:

```
<Action> [<Object>] [<Preposition> <Target>] [<Condition>].
```

### Core Action Verbs

#### Variable Operations
- **Create/Make/Define**: Create variables
  - `Create a variable called x with value 5.`
  - `Make a list called numbers.`
  
- **Set/Store/Save**: Assign values
  - `Set x to 10.`
  - `Store the result in total.`
  - `Save username as "Alice".`

- **Add/Subtract/Multiply/Divide**: Arithmetic
  - `Add 5 to x.`
  - `Multiply a and b and store in product.`
  - `Increment counter.`
  - `Decrement remaining.`

#### Input/Output
- **Ask/Get/Prompt**: User input
  - `Ask the user for their name.`
  - `Get a number from the user and store it in age.`
  - `Prompt for password without showing it.`

- **Display/Show/Print/Say**: Output
  - `Display "Hello World".`
  - `Show the value of x.`
  - `Print result followed by " items".`

#### Control Flow
- **If/When**: Conditionals
  - `If x is greater than 10, display "Big".`
  - `If age is less than 18, display "Minor". Otherwise display "Adult".`
  - `When status equals "ready", start processing.`

- **Repeat/Loop/For/While**: Iteration
  - `Repeat 10 times: increment counter.`
  - `While x is less than 100: multiply x by 2.`
  - `For each item in list: display item.`
  - `Loop until user says "quit".`

- **Stop/Break/Continue**: Flow control
  - `Stop the loop.`
  - `Continue to next iteration.`
  - `Exit the function.`

#### Functions
- **Create function/Define function**: Function declaration
  - `Create function add that takes a and b.`
  - `Define function greet with parameter name.`

- **Call/Run/Execute**: Function invocation
  - `Call add with 5 and 10.`
  - `Run process_data with input_file.`

- **Return**: Function returns
  - `Return the result.`
  - `Return true if found.`

#### Data Structures
- **List/Array operations**:
  - `Add item to list.`
  - `Remove item from list.`
  - `Get item at index 3 from list.`
  - `The length of list.`

- **Dictionary/Map operations**:
  - `Create a dictionary called user.`
  - `Set key "name" to "Alice" in user.`
  - `Get value for key "age" from user.`

#### File Operations
- **Read/Load**: File input
  - `Read file "data.txt" into content.`
  - `Load JSON from "config.json" into settings.`

- **Write/Save**: File output
  - `Write text to file "output.txt".`
  - `Save data as JSON to "result.json".`

### Data Types (Inferred)

- **Numbers**: Integers and floats
  - `5`, `3.14`, `-42`
  
- **Strings**: Text in quotes
  - `"Hello"`, `'World'`, `"Multi-word string"`

- **Booleans**: Logical values
  - `true`, `false`, `yes`, `no`

- **Lists**: Ordered collections
  - `[1, 2, 3]`, `["a", "b", "c"]`

- **Dictionaries**: Key-value pairs
  - `{"name": "Alice", "age": 30}`

- **None/Null**: Absence of value
  - `nothing`, `null`, `none`

### Operators

#### Comparison
- `is equal to`, `equals`, `==`
- `is not equal to`, `!=`
- `is greater than`, `>`, `is more than`
- `is less than`, `<`
- `is greater than or equal to`, `>=`
- `is less than or equal to`, `<=`

#### Logical
- `and`, `&&`
- `or`, `||`
- `not`, `!`

#### Arithmetic
- `plus`, `+`, `add`
- `minus`, `-`, `subtract`
- `times`, `*`, `multiply`
- `divided by`, `/`, `divide`
- `modulo`, `%`, `remainder`
- `to the power of`, `**`, `^`

### Comments

```
# This is a single-line comment

Note: This is also a comment.

# Multi-line explanations
# can span multiple lines
```

## Scoping Rules

1. **Global Scope**: Variables defined outside functions
2. **Function Scope**: Parameters and local variables
3. **Block Scope**: Variables in loops/conditionals (inherit parent scope)
4. **Shadowing**: Inner scopes can shadow outer variables

## Execution Model

### Phase 1: Parsing
1. Tokenize English sentences
2. Apply NLP to extract intent (verb, objects, modifiers)
3. Build Abstract Syntax Tree (AST)
4. Validate semantic correctness

### Phase 2: Analysis
1. Type inference
2. Variable resolution
3. Control flow analysis
4. Optimize patterns (constant folding, dead code elimination)

### Phase 3: IR Generation
1. Convert AST to Logic Graph
2. Nodes represent operations
3. Edges represent data/control flow
4. Graph is serializable and inspectable

### Phase 4: Execution
- **Interpreter Mode**: Walk graph, execute nodes
- **Compiler Mode**: Transpile to C/LLVM IR, compile to native binary

## Error Handling

### Syntax Errors
```
"Multiply x by" - Missing operand
→ "Did you mean: 'Multiply x by [value]'?"
```

### Runtime Errors
```
Dividing by zero detected
→ "Division by zero at line 10. Check your divisor value."
```

### Type Errors
```
Cannot add string "hello" to number 5
→ "Type mismatch: trying to add text and number. Convert one to match the other."
```

## Advanced Features

### Async/Concurrency
```
Run these tasks in parallel:
  - Fetch data from API
  - Load local cache
  - Process user input
Wait for all tasks to complete.
```

### Exception Handling
```
Try to read file "data.txt".
If there's an error, display "File not found" and use default data.
```

### Modules/Import
```
Import math functions from standard library.
Use sqrt function with 16.
```

### Classes/OOP
```
Create a class called Dog with properties name and age.
Define method bark that displays "Woof!".
Create a new Dog called buddy with name "Buddy" and age 3.
Call bark on buddy.
```

## Built-in Functions

- **Math**: sqrt, abs, round, floor, ceil, sin, cos, tan, log, exp
- **String**: length, uppercase, lowercase, substring, split, join, replace
- **List**: append, remove, sort, filter, map, reduce
- **I/O**: read_file, write_file, read_line, print
- **Type**: type_of, convert_to_int, convert_to_float, convert_to_string
- **Time**: current_time, sleep, timestamp
- **Random**: random_number, random_choice, shuffle

## Optimization Hints

Users can provide hints for performance:

```
Optimize this loop for speed.
Use parallel processing for this section.
Cache the result of this expensive function.
```

## Interoperability

### Calling External Code
```
Import Python library numpy as np.
Call np.array with [1, 2, 3] and store in arr.
```

### Exporting Functions
```
Export function calculate as C library.
```

## Examples

### Hello World
```
Display "Hello, World!".
```

### User Input
```
Ask the user for their name and store it in username.
Display "Hello, " followed by username followed by "!".
```

### Conditional
```
Ask the user for a number and store it in x.
If x is greater than 0, display "Positive".
Otherwise if x is less than 0, display "Negative".
Otherwise display "Zero".
```

### Loop
```
Create a variable called i with value 1.
Repeat while i is less than or equal to 10:
  Display the value of i.
  Increment i.
```

### Function
```
Create function factorial that takes n.
  If n is less than or equal to 1, return 1.
  Otherwise:
    Calculate factorial with n minus 1 and store in result.
    Multiply result by n.
    Return result.

Call factorial with 5 and display the result.
```

### List Processing
```
Create a list called numbers with values [1, 2, 3, 4, 5].
Create an empty list called doubled.
For each num in numbers:
  Multiply num by 2 and add it to doubled.
Display doubled.
```

### File I/O
```
Read file "input.txt" into content.
Convert content to uppercase and store in upper.
Write upper to file "output.txt".
Display "Done!".
```

### Web Server (Advanced)
```
Import web framework.
Create a web server on port 8080.
Define route "/" with handler:
  Return "Welcome to Vyra!".
Define route "/api/greet" with handler that takes name parameter:
  Return "Hello, " followed by name.
Start the server and display "Server running on port 8080".
```

## Future Extensions

- Pattern matching
- Generators/yields
- Decorators
- Macros
- Type annotations (optional)
- Gradual typing
- Domain-specific sublanguages (SQL-like, Regex in English)

---

**Version**: 1.0  
**Last Updated**: December 24, 2025  
**Status**: Stable
