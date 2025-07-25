# 🧮 Simple Calculator Project

This project contains two different calculator implementations: a command-line version and a web-based version. Both calculators perform basic arithmetic operations with a clean, user-friendly interface.

## 📁 Files Overview

- **`calculator.py`** - Command-line calculator with Python
- **`calculator.html`** - Web-based calculator with HTML/CSS/JavaScript
- **`test_calculator.py`** - Test script demonstrating calculator functionality

## 🚀 How to Use

### Command-Line Calculator (`calculator.py`)

**Run the calculator:**
```bash
python3 calculator.py
```

**Features:**
- ✅ Basic arithmetic: `+`, `-`, `*`, `/`
- ✅ Exponentiation: `^` or `**`
- ✅ Square root: `sqrt(number)`
- ✅ Parentheses for order of operations: `(`, `)`
- ✅ Calculation history
- ✅ Error handling (division by zero, invalid input)

**Example commands:**
```
Enter calculation: 2+3
Result: 5

Enter calculation: sqrt(16)
Result: 4.0

Enter calculation: (10+5)*2
Result: 30

Enter calculation: history
--- Calculation History ---
1. 2+3 = 5
2. math.sqrt(16) = 4.0
3. (10+5)*2 = 30
```

**Control commands:**
- `help` - Show menu
- `history` - Display calculation history
- `clear` - Clear history
- `quit` or `exit` - Exit calculator

### Web Calculator (`calculator.html`)

**Run the web calculator:**
```bash
# Open calculator.html in your web browser
# Or serve it with a simple HTTP server:
python3 -m http.server 8000
# Then visit: http://localhost:8000/calculator.html
```

**Features:**
- 🖱️ Click buttons or use keyboard input
- ✅ Beautiful, modern UI with animations
- ✅ Basic arithmetic operations
- ✅ Square root function
- ✅ Clear (C) and Clear Entry (CE) buttons
- ✅ Calculation history with toggle view
- ✅ Error handling and validation
- 📱 Responsive design for mobile devices

**Keyboard shortcuts:**
- `0-9`, `.` - Numbers and decimal
- `+`, `-`, `*`, `/` - Operators
- `Enter` or `=` - Calculate result
- `Escape` or `C` - Clear all
- `Backspace` - Delete last digit

## 🔧 How It Works

### Python Calculator Architecture

The command-line calculator uses object-oriented programming:

```python
class Calculator:
    def __init__(self):
        self.history = []  # Store calculation history
    
    def evaluate_expression(self, expression):
        # Safely parse and evaluate mathematical expressions
        # Uses Python's eval() with restricted environment
        # Supports: +, -, *, /, **, sqrt(), parentheses
```

**Key Components:**

1. **Expression Parsing**: Uses regex to safely handle `sqrt()` functions
2. **Security**: Restricts `eval()` to prevent code injection
3. **Error Handling**: Catches division by zero and invalid expressions
4. **History Management**: Stores and displays previous calculations

### Web Calculator Architecture

The web calculator uses vanilla JavaScript with state management:

```javascript
// Calculator state variables
let currentInput = '0';
let previousInput = '';
let operator = '';
let waitingForOperand = false;
let history = [];
```

**Key Components:**

1. **State Management**: Tracks current/previous inputs and operations
2. **Event Handling**: Mouse clicks and keyboard input
3. **DOM Manipulation**: Updates display and history dynamically
4. **CSS Grid Layout**: Responsive button arrangement
5. **Error Prevention**: Input validation and error messages

### Calculation Flow

**Both calculators follow this pattern:**

1. **Input**: Receive user input (numbers/operators)
2. **Parsing**: Convert input into executable format
3. **Validation**: Check for errors (division by zero, invalid syntax)
4. **Calculation**: Perform the mathematical operation
5. **Display**: Show result to user
6. **History**: Store calculation for future reference

## 🧪 Testing

Run the test script to see the calculator in action:

```bash
python3 test_calculator.py
```

This will demonstrate various calculations and show how the history feature works.

## 🛡️ Security Features

### Python Calculator
- **Safe Evaluation**: Uses restricted `eval()` environment
- **Input Sanitization**: Validates characters before evaluation
- **Error Boundaries**: Catches and handles all exceptions

### Web Calculator
- **No Eval Usage**: Uses mathematical operations instead of `eval()`
- **Input Validation**: Prevents invalid character entry
- **Type Checking**: Ensures numeric operations only

## 🎨 Design Principles

1. **User-Friendly**: Clear interface and helpful error messages
2. **Robust**: Handles edge cases and invalid input gracefully
3. **Extensible**: Easy to add new operations or features
4. **Educational**: Code is well-commented for learning

## 🔮 Possible Extensions

- Scientific functions (sin, cos, tan, log)
- Memory functions (M+, M-, MR, MC)
- Unit conversions
- Multi-line expressions
- Graphing capabilities
- Expression history with re-evaluation

---

**Happy calculating! 🎉**