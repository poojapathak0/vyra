# 🚀 Vyra - Programming in Plain English

**Vyra** is a programming language where you write code in natural, human-readable English sentences.

## ✨ Why Vyra?

- **Zero Syntax Barriers**: Write code like you think
- **Practical**: Great for learning, scripting, and small CLI tools
- **Deterministic**: Same input → same output (logic-graph execution)
- **Educational**: Perfect for CS students and beginners
- **Extensible**: Add new sentence patterns and built-ins in Python

## 🎯 Example

```vyra
Ask the user for their name and store it in username.
Display "Hello, " followed by username followed by "!".
Ask the user for two numbers called a and b.
Add a and b and store the result in sum.
If sum is greater than 10, display "Large number!".
Otherwise display "Small number.".
```

## 🏗️ Features

- **Natural Language Syntax**: Write imperative instructions in plain English
- **Smart Parsing**: Rule-based parser with a deterministic logic-graph IR
- **Interpreter Runtime**: Executes graphs with scoped variables and functions
- **Core Language**: Variables, arithmetic, I/O, conditionals, loops, lists, functions, file I/O
- **Debuggable**: Optional graph visualization + debug mode (where available)

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Your First Program

```bash
python -m vyra run examples/hello.intent
```

### Optional: AI Rewrite Mode (off by default)

Vyra can optionally send your source to an external LLM to rewrite "free-form English" into canonical Vyra code *before* parsing.

- Enable per command: `vyra run --ai program.intent`, `vyra parse --ai program.intent`, or `vyra repl --ai`
- Configure via environment variables:
     - `VYRA_AI_URL` = OpenAI-compatible Chat Completions endpoint URL
     - `VYRA_AI_MODEL` = model name
     - `VYRA_AI_API_KEY` = optional (required by many hosted APIs)
     - `VYRA_AI_PROVIDER` = `openai_compatible` (default)
     - `VYRA_AI_TIMEOUT` = request timeout seconds (default 30)

If `--ai` is enabled but the required variables are missing, Vyra prints an AI rewrite error and exits.

### Interactive REPL

```bash
python -m vyra repl
``` 



## 📚 Documentation

- [Language Specification](docs/SPECIFICATION.md)
- [Tutorial](docs/TUTORIAL.md)
- [Quick Reference](docs/QUICKREF.md)
- [Examples](examples/)
- [Contributing](CONTRIBUTING.md)

## 🎮 Example Programs

- **Hello World**: [examples/hello.intent](examples/hello.intent)
- **Calculator**: [examples/calculator.intent](examples/calculator.intent)
- **Functions**: [examples/functions.intent](examples/functions.intent)
- **Game**: [examples/number_game.intent](examples/number_game.intent)
- **Lists**: [examples/list_processing.intent](examples/list_processing.intent)
- **Fibonacci**: [examples/fibonacci.intent](examples/fibonacci.intent)
- **File I/O**: [examples/file_io.intent](examples/file_io.intent)
- **Greeting**: [examples/greeting.intent](examples/greeting.intent)
- **Temperature**: [examples/temperature.intent](examples/temperature.intent)

## 🏛️ Architecture

```
┌─────────────────┐
│ English Source  │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Parser │ (NLP + Rules)
    └────┬────┘
         │
    ┌────▼────────┐
    │ Logic Graph │ (Intermediate Representation)
    └────┬────────┘
         │
    ┌────▼─────────┐
    │  Interpreter │ or ┌──────────┐
    │   Engine     │    │ Compiler │ → Native Code
    └──────────────┘    └──────────┘
```

## ⚡ Performance

Vyra currently runs via an interpreter.
A native compiler (LLVM/AOT) is a future roadmap item.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🌟 Roadmap

- [ ] Mobile app IDE
- [ ] GPU acceleration for ML workloads
- [ ] Visual programming interface
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Embedded systems target
- [ ] Real-time collaboration
- [ ] Blockchain integration



---

**Made with ❤️ by the Vyra community**

*Transform your ideas into code at the speed of thought.*
