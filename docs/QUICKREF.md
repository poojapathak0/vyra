# Vyra Quick Reference

## Basic Syntax

### Variables
```vyra
Set x to 5.
Create a variable called name with value "Alice".
Store 10 in count.
```

### Output
```vyra
Display "Hello".
Show the value of x.
Print result followed by " items".
```

### Input
```vyra
Ask the user for their name.
Get a number from the user and store it in age.
```

## Arithmetic

```vyra
Add 5 and 10 and store the result in sum.
Multiply a and b and store the result in product.
Add 3 to x.
Subtract 2 from total.
Increment counter.
Decrement remaining.
```

## Conditionals

```vyra
If x is greater than 10:
  Display "Big".
Otherwise:
  Display "Small".
```

### Comparison Operators
- `is equal to`, `equals`
- `is not equal to`
- `is greater than`, `>`
- `is less than`, `<`
- `is greater than or equal to`, `>=`
- `is less than or equal to`, `<=`

## Loops

### Repeat N Times
```vyra
Repeat 10 times:
  Display "Hello".
```

### While Loop
```vyra
While x is less than 100:
  Multiply x by 2.
```

### For-Each Loop
```vyra
For each item in list:
  Display item.
```

### Loop Control
```vyra
Stop the loop.
Continue to next iteration.
```

## Lists

```vyra
Create a list called numbers with values [1, 2, 3].
Add item to list.
For each num in numbers:
  Display num.
```

## Functions

```vyra
Create function greet that takes name:
  Display "Hello, " followed by name.

Call greet with "Alice".
```

## File I/O

```vyra
Read file "data.txt" into content.
Write text to file "output.txt".
```

## Multi-file Programs (Include)

```vyra
Include "utils.vyra".
Display "Loaded".
```

## Python Bridge (Optional)

Call allowlisted Python functions (disabled by default):

```vyra
Set r to call py_call with "math" and "sqrt" and 16.
Display the value of r.
```

Enable with env vars:
- `VYRA_PY_BRIDGE=1`
- `VYRA_PY_ALLOW=math,json`

## Comments

```vyra
# Single-line comment
Note: This is also a comment.
```

## Built-in Functions

- `length` / `len` - Get length of string/list
- `abs` - Absolute value
- `round` - Round number
- String operations: `uppercase`, `lowercase`, `split`, `join`

## CLI Commands

```bash
# Run a program
python -m vyra run program.vyra

# Start REPL
python -m vyra repl

# Debug mode
python -m vyra run --debug program.vyra

# Visualize graph
python -m vyra run --viz program.vyra

# Parse only
python -m vyra parse program.vyra

# Optional AI rewrite
python -m vyra run --ai program.vyra
```

Note: `.vyra` is the recommended file extension. `.intent` is still supported for backward compatibility.

## Common Patterns

### Input Validation
```vyra
Set valid to false.
While valid is equal to false:
  Ask the user for age called age.
  If age is greater than 0:
    Set valid to true.
  Otherwise:
    Display "Invalid age!".
```

### Accumulator
```vyra
Set sum to 0.
For each num in numbers:
  Add num to sum.
```

### Counter Loop
```vyra
Set i to 1.
While i is less than or equal to 10:
  Display i.
  Increment i.
```

### Error Handling
```vyra
If divisor is equal to 0:
  Display "Error: Cannot divide by zero!".
Otherwise:
  Divide a by divisor and store in result.
```
