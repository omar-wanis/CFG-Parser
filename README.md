# CFG-Parser

A Python project for parsing and analyzing Context-Free Grammars (CFGs), featuring both a command-line backend and a modern graphical user interface (GUI) built with `customtkinter`. The parser supports string validation using both BFS and DFS derivation methods, making it a useful tool for students, educators, and anyone interested in formal language processing.

## Features

- **Define your own CFG:** Enter grammar rules in a user-friendly format.
- **Parse strings:** Check if a string is accepted by your grammar using either BFS or DFS.
- **Visualize derivation paths:** See the derivation steps for accepted strings.
- **GUI and CLI support:** Use the graphical interface or run parsing directly from Python.
- **Customizable terminals, variables, and null (epsilon) character.**

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/omar-wanis/CFG-Parser.git
   cd CFG-Parser
   ```

2. **Install Python dependencies:**

   ```
   pip install customtkinter prettytable
   ```

## Usage

### GUI

Run the GUI app with:

```bash
python "CFG Parser/GUI.py"
```

- **Grammar entry:** Type rules (e.g., `S -> 0S1 | 0S0 | 0 | 1`) and finish entry.
- **Parse strings:** Enter a string and choose DFS or BFS parsing.
- **Derivation visualization:** Accepted strings will display the derivation path.

### Command Line / Module

You can use the parser programmatically:

```python
from CFGParser import CFG

# Define your grammar
g = CFG(
    terminals={'0', '1', 'λ'}, 
    rules={'S': ['0S', '1S', '0', '1']}
)
g.rules(None)  # Prepare rules

# Parse a string using BFS
result, node = g.BFS("001")
print(f"Accepted? {result}")

# See derivation path if accepted
if result:
    print(g.Derivation_Path(node))
```

## Grammar Rules Format

- Use uppercase for variables (non-terminals), e.g., `S`.
- Separate productions with `|`, e.g., `S -> 0S | 1S | 0 | 1`.
- Use `λ` or `ε` for the null/epsilon character.
- Only uppercase variables are allowed on the left side of a rule.

## Project Structure

```
CFG-Parser/
│
├── CFG Parser/
│   ├── CFGParser.py   # Main parser logic and algorithms
│   └── GUI.py         # CustomTkinter-based UI
└── README.md
```

## Dependencies

- Python 3.x
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- prettytable

## Credits

Developed by [omar-wanis](https://github.com/omar-wanis).

## License

This project is open source. See [LICENSE](LICENSE) for details.
