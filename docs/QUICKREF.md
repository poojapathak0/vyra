# IntentLang Quick Reference

## Basic Syntax

### Variables
```intentlang
Set x to 5.
Create a variable called name with value "Alice".
Store 10 in count.
```

### Output
```intentlang
Display "Hello".
Show the value of x.
Print result followed by " items".
```

### Input
```intentlang
Ask the user for their name.
Get a number from the user and store it in age.
```

## Arithmetic

```intentlang
Add 5 and 10 and store the result in sum.
Multiply a and b and store the result in product.
Add 3 to x.
Subtract 2 from total.
Increment counter.
Decrement remaining.
```

## Conditionals

```intentlang
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
```intentlang
Repeat 10 times:
  Display "Hello".
```

### While Loop
```intentlang
While x is less than 100:
  Multiply x by 2.
```

### For-Each Loop
```intentlang
For each item in list:
  Display item.
```

### Loop Control
```intentlang
Stop the loop.
Continue to next iteration.
```

## Lists

```intentlang
Create a list called numbers with values [1, 2, 3].
Add item to list.
For each num in numbers:
  Display num.
```

## Functions

```intentlang
Create function greet that takes name:
  Display "Hello, " followed by name.

Call greet with "Alice".
```

## File I/O

```intentlang
Read file "data.txt" into content.
Write text to file "output.txt".
```

## Comments

```intentlang
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
python -m intentlang run program.intent

# Start REPL
python -m intentlang repl

# Debug mode
python -m intentlang run --debug program.intent

# Visualize graph
python -m intentlang run --viz program.intent

# Parse only
python -m intentlang parse program.intent
```

## Common Patterns

### Input Validation
```intentlang
Set valid to false.
While valid is equal to false:
  Ask the user for age called age.
  If age is greater than 0:
    Set valid to true.
  Otherwise:
    Display "Invalid age!".
```

### Accumulator
```intentlang
Set sum to 0.
For each num in numbers:
  Add num to sum.
```

### Counter Loop
```intentlang
Set i to 1.
While i is less than or equal to 10:
  Display i.
  Increment i.
```

### Error Handling
```intentlang
If divisor is equal to 0:
  Display "Error: Cannot divide by zero!".
Otherwise:
  Divide a by divisor and store in result.
```
