# IntentLang Tutorial

Welcome to IntentLang! This tutorial will teach you how to write code in plain English.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Concepts](#basic-concepts)
3. [Variables](#variables)
4. [Input and Output](#input-and-output)
5. [Arithmetic](#arithmetic)
6. [Conditionals](#conditionals)
7. [Loops](#loops)
8. [Lists](#lists)
9. [Functions](#functions)
10. [File Operations](#file-operations)

## Getting Started

Create a new file with the `.intent` extension (e.g., `myprogram.intent`) and start writing!

### Your First Program

```intentlang
Display "Hello, World!".
```

Run it:
```bash
python -m intentlang run myprogram.intent
```

## Basic Concepts

### Sentences as Code

Every statement in IntentLang is a sentence. Each sentence:
- Starts with an action verb (Display, Set, Ask, etc.)
- Ends with a period (`.`)
- Reads like an instruction to a human

### Comments

Add comments to explain your code:

```intentlang
# This is a single-line comment

Note: This is also a comment!

Display "Hello".  # Comments can go at the end too
```

## Variables

### Creating Variables

```intentlang
Set x to 5.
Create a variable called name with value "Alice".
Define age as 25.
```

### Variable Names

Use descriptive names:
- `username`, `total_price`, `item_count` ✓
- `x`, `temp`, `val` (okay for simple cases)

## Input and Output

### Output (Displaying)

```intentlang
Display "Hello!".
Show the value of x.
Print "The result is: " followed by result.
```

### Input (Asking)

```intentlang
Ask the user for their name.
Get a number from the user and store it in age.
Prompt for password without showing it.
```

## Arithmetic

### Basic Operations

```intentlang
Add 5 and 10 and store the result in sum.
Multiply a and b and store the result in product.

Add 3 to x.
Subtract 2 from total.
Multiply score by 2.
Divide amount by 4.
```

### Increment and Decrement

```intentlang
Increment counter.
Decrement remaining.
```

## Conditionals

### If Statements

```intentlang
If age is greater than 18:
  Display "Adult".
```

### If-Else

```intentlang
If temperature is greater than 30:
  Display "Hot day!".
Otherwise:
  Display "Nice weather.".
```

### Nested Conditions

```intentlang
If score is greater than or equal to 90:
  Display "Grade: A".
Otherwise if score is greater than or equal to 80:
  Display "Grade: B".
Otherwise if score is greater than or equal to 70:
  Display "Grade: C".
Otherwise:
  Display "Grade: F".
```

### Comparison Operators

- `is equal to`, `equals`, `is`
- `is not equal to`
- `is greater than`, `is more than`
- `is less than`
- `is greater than or equal to`, `is at least`
- `is less than or equal to`, `is at most`

## Loops

### Repeat N Times

```intentlang
Repeat 10 times:
  Display "Hello".
```

### While Loop

```intentlang
Set i to 1.
While i is less than or equal to 5:
  Display the value of i.
  Increment i.
```

### For-Each Loop

```intentlang
Create a list called items with values [1, 2, 3, 4, 5].
For each item in items:
  Display item.
```

### Loop Control

```intentlang
While true:
  Ask the user for input called cmd.
  If cmd equals "quit":
    Stop the loop.
  Display "You entered: " followed by cmd.
```

## Lists

### Creating Lists

```intentlang
Create a list called numbers with values [1, 2, 3].
Create an empty list called items.
```

### Adding to Lists

```intentlang
Add 42 to numbers.
Append value to items.
```

### Processing Lists

```intentlang
For each num in numbers:
  Multiply num by 2 and store in doubled.
  Display doubled.
```

## Functions

### Defining Functions

```intentlang
Create function greet that takes name:
  Display "Hello, " followed by name followed by "!".

Define function add with parameters a and b:
  Add a and b and store in result.
  Return result.
```

### Calling Functions

```intentlang
Call greet with "Alice".
Call add with 5 and 10 and store in sum.
```

## File Operations

### Reading Files

```intentlang
Read file "data.txt" into content.
Display the value of content.
```

### Writing Files

```intentlang
Set message to "Hello from IntentLang!".
Write message to file "output.txt".
```

## Best Practices

### 1. Use Descriptive Names

```intentlang
# Good
Set user_age to 25.
Set total_price to 99.99.

# Less clear
Set x to 25.
Set t to 99.99.
```

### 2. Add Comments

```intentlang
# Calculate the average of three numbers
Add num1 and num2 and store in sum.
Add sum and num3 and store in total.
Divide total by 3 and store in average.
```

### 3. Break Down Complex Logic

```intentlang
# Instead of complex nested conditions, use clear steps:

# Step 1: Check age category
If age is less than 13:
  Set category to "child".
Otherwise if age is less than 20:
  Set category to "teen".
Otherwise:
  Set category to "adult".

# Step 2: Apply category-specific logic
If category equals "child":
  Set ticket_price to 5.
```

### 4. Handle Edge Cases

```intentlang
Ask the user for a divisor called divisor.

If divisor is equal to 0:
  Display "Error: Cannot divide by zero!".
Otherwise:
  Divide 100 by divisor and store in result.
  Display "Result: " followed by result.
```

## Common Patterns

### Input Validation

```intentlang
Set valid to false.
While valid is equal to false:
  Ask the user for age called age.
  If age is greater than 0 and age is less than 150:
    Set valid to true.
  Otherwise:
    Display "Please enter a valid age (1-150).".
```

### Menu System

```intentlang
Display "Menu:".
Display "1. Option A".
Display "2. Option B".
Display "3. Exit".

Ask the user for choice called choice.

If choice equals 1:
  Display "You selected Option A".
If choice equals 2:
  Display "You selected Option B".
If choice equals 3:
  Display "Goodbye!".
```

### Accumulator Pattern

```intentlang
Set sum to 0.
For each number in numbers:
  Add number to sum.
Display "Total: " followed by sum.
```

## Next Steps

1. Try the examples in the `examples/` folder
2. Build your own programs
3. Experiment with combinations of features
4. Read the [Language Specification](SPECIFICATION.md) for advanced features

## Getting Help

- Check the [FAQ](FAQ.md)
- Read the [API Reference](API.md)
- Join our [Discord community](#)
- Open an issue on [GitHub](#)

---

**Happy coding in plain English! 🚀**
