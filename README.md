# 🚀 Vyra - Programming in Plain English

**Vyra** is a programming language where you write code in natural, human-readable English sentences.

## ✨ Why Vyra?

- **Zero Syntax Barriers**: Write code like you think
- **Blazing Fast**: Compiles to native code, performs like C++
- **Universal**: Build anything—web apps, ML models, games, servers
- **Educational**: Perfect for CS students and beginners
- **Production-Ready**: Robust error handling, optimizations, and extensibility

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
- **Smart Parsing**: NLP-powered with deterministic logic graphs
- **High Performance**: LLVM-based compilation with -O3 optimizations
- **Multi-Paradigm**: Imperative, functional, and OOP—all in natural terms
- **Rich Ecosystem**: Built-in support for web, ML, data science, concurrency
- **Educational Tools**: Code explanations, flow visualizations, gamification
- **Robust**: Handles ambiguities, typos, edge cases gracefully

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Your First Program

```bash
python -m vyra run examples/hello.intent
```

### Interactive REPL

```bash
python -m vyra repl
```

## 📚 Documentation

- [Language Specification](docs/SPECIFICATION.md)
- [Tutorial](docs/TUTORIAL.md)
- [Examples](examples/)
- [API Reference](docs/API.md)
- [Contributing](CONTRIBUTING.md)

## 🎮 Example Programs

- **Calculator**: [examples/calculator.intent](examples/calculator.intent)
- **Web Server**: [examples/webserver.intent](examples/webserver.intent)
- **Machine Learning**: [examples/ml_classifier.intent](examples/ml_classifier.intent)
- **Game**: [examples/number_game.intent](examples/number_game.intent)
- **Data Processing**: [examples/data_analysis.intent](examples/data_analysis.intent)

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

## 🎨 IDE

Launch the web-based IDE:

```bash
cd ide
npm install
npm run dev
```

Features:
- Live parsing and syntax feedback
- Logic graph visualization
- Dark mode with smooth animations
- Collaborative editing
- Voice-to-code input

## ⚡ Performance

Vyra aims for near-C++ performance:
- **Fibonacci(35)**: ~2x slower than C++ (optimized)
- **Matrix operations**: ~1.5x slower than NumPy
- **Web serving**: Comparable to Node.js

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
