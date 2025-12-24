# Contributing to IntentLang

Thank you for your interest in contributing to IntentLang! This document provides guidelines for contributing to the project.

## 🌟 Ways to Contribute

- **Report Bugs**: Found a bug? Open an issue!
- **Suggest Features**: Have an idea? We'd love to hear it!
- **Write Documentation**: Help others learn IntentLang
- **Submit Code**: Fix bugs or implement features
- **Create Examples**: Share cool programs you've written
- **Spread the Word**: Tell others about IntentLang

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/intentlang.git
cd intentlang
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### 4. Create a Branch

```bash
git checkout -b feature/my-awesome-feature
```

## 📝 Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=intentlang --cov-report=html

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

### Code Style

We use `black` for code formatting and `flake8` for linting:

```bash
# Format code
black intentlang/ tests/

# Check linting
flake8 intentlang/ tests/

# Type checking
mypy intentlang/
```

### Testing Your Changes

Before submitting, ensure:

1. All tests pass: `pytest`
2. Code is formatted: `black .`
3. No lint errors: `flake8`
4. Add tests for new features
5. Update documentation as needed

### Running IntentLang Programs

```bash
# Test your changes with example programs
python -m intentlang run examples/hello.intent
python -m intentlang run examples/calculator.intent

# Try the REPL
python -m intentlang repl
```

## 🎯 Contribution Guidelines

### Code Quality

- Write clear, readable code
- Add docstrings to functions and classes
- Include type hints where appropriate
- Follow PEP 8 style guidelines
- Keep functions small and focused

### Testing

- Write tests for new features
- Ensure edge cases are covered
- Test both success and failure paths
- Aim for >80% code coverage

### Documentation

- Update README.md if adding major features
- Add docstrings to all public APIs
- Update TUTORIAL.md for user-facing changes
- Include examples in docstrings

### Commit Messages

Write clear, descriptive commit messages:

```
Add support for dictionary operations

- Implement dict access and set nodes
- Add parser patterns for dict operations
- Include tests for dict functionality
- Update specification with dict syntax
```

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Pull Request Process

1. **Update your branch**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes**:
   ```bash
   git push origin feature/my-awesome-feature
   ```

3. **Open a Pull Request** on GitHub

4. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

5. **Address review feedback**

6. **Wait for approval** from maintainers

## 🐛 Reporting Bugs

### Before Reporting

- Search existing issues to avoid duplicates
- Try to reproduce with latest version
- Gather relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Write this code: '...'
2. Run with: '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Code sample**
```intentlang
# Minimal code that reproduces the issue
Display "Hello".
```

**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python version: [e.g., 3.10.5]
- IntentLang version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
How should the feature work?

**Example usage**
```intentlang
# Show how the feature would be used
```

**Alternatives considered**
Other approaches you've thought about.

**Additional context**
Screenshots, mockups, related features, etc.
```

## 🏗️ Architecture Overview

```
intentlang/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── parser.py            # English → AST parser
├── ast_nodes.py         # AST node definitions
├── logic_graph.py       # AST → Graph IR
├── interpreter.py       # Graph execution engine
```

### Key Components

**Parser**: Converts English sentences to Abstract Syntax Tree
- Uses regex patterns for action recognition
- Handles natural language variations
- Extensible pattern system

**Logic Graph**: Intermediate representation
- Nodes = operations (assign, if, loop, etc.)
- Edges = control flow
- Serializable for visualization/debugging

**Interpreter**: Executes logic graphs
- Graph traversal with state management
- Scoped variable handling
- Built-in function support

## 🎨 Adding New Features

### Adding a New Statement Type

1. **Define AST Node** (`ast_nodes.py`):
   ```python
   @dataclass
   class NewStatementNode(ASTNode):
       property: str = ""
   ```

2. **Add Parser Pattern** (`parser.py`):
   ```python
   'new_action': [
       (r'pattern to match (.+)', 'action_type'),
   ]
   ```

3. **Implement Parser Handler** (`parser.py`):
   ```python
   elif action_type == 'action_type':
       return NewStatementNode(...)
   ```

4. **Add Graph Builder** (`logic_graph.py`):
   ```python
   def visit_new_statement(self, node, from_node_id):
       # Build graph nodes
   ```

5. **Implement Execution** (`interpreter.py`):
   ```python
   def _execute_new_statement(self, graph, node):
       # Execute the statement
   ```

6. **Add Tests**:
   ```python
   def test_new_statement(self):
       code = "New statement pattern."
       ast = self.parser.parse(code)
       assert isinstance(ast.statements[0], NewStatementNode)
   ```

7. **Update Documentation**:
   - Add to `SPECIFICATION.md`
   - Include examples in `TUTORIAL.md`

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Writing Great Git Commit Messages](https://chris.beams.io/posts/git-commit/)
- [NetworkX Documentation](https://networkx.org/)
- [AST Design Patterns](https://en.wikipedia.org/wiki/Abstract_syntax_tree)

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behaviors:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 📞 Getting Help

- **Discord**: Join our community server
- **GitHub Discussions**: Ask questions and share ideas
- **Email**: contact@intentlang.org
- **Stack Overflow**: Tag your questions with `intentlang`

## 🙏 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation

Thank you for helping make IntentLang better! 🎉

---

**Happy Contributing!** 🚀
