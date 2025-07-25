#!/usr/bin/env python3
"""
Simple Calculator
A command-line calculator that performs basic arithmetic operations.
"""

import re
import math

class Calculator:
    """A simple calculator class with basic arithmetic operations."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Addition operation."""
        return a + b
    
    def subtract(self, a, b):
        """Subtraction operation."""
        return a - b
    
    def multiply(self, a, b):
        """Multiplication operation."""
        return a * b
    
    def divide(self, a, b):
        """Division operation with zero-division check."""
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    
    def power(self, a, b):
        """Exponentiation operation."""
        return a ** b
    
    def square_root(self, a):
        """Square root operation."""
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number!")
        return math.sqrt(a)
    
    def evaluate_expression(self, expression):
        """
        Safely evaluate a mathematical expression.
        Supports: +, -, *, /, **, (), sqrt()
        """
        # Remove whitespace
        expression = expression.replace(" ", "")
        
        # Replace sqrt() function
        expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
        
        # Validate expression (only allow safe characters)
        allowed_chars = set('0123456789+-*/().^')
        if not all(c in allowed_chars or c.isspace() for c in expression.replace('math.sqrt', '')):
            raise ValueError("Invalid characters in expression!")
        
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        
        try:
            # Safely evaluate the expression
            result = eval(expression, {"__builtins__": {}, "math": math})
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def show_history(self):
        """Display calculation history."""
        if not self.history:
            print("No calculations in history.")
            return
        
        print("\n--- Calculation History ---")
        for i, calc in enumerate(self.history, 1):
            print(f"{i}. {calc}")
        print()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()
        print("History cleared!")

def print_menu():
    """Display the calculator menu."""
    print("\n" + "="*50)
    print("           SIMPLE CALCULATOR")
    print("="*50)
    print("Commands:")
    print("  • Enter any mathematical expression")
    print("  • Supported operations: +, -, *, /, ^, sqrt()")
    print("  • Examples: 2+3, 10*5, sqrt(16), 2^3")
    print("  • 'history' - Show calculation history")
    print("  • 'clear' - Clear history")
    print("  • 'help' - Show this menu")
    print("  • 'quit' or 'exit' - Exit calculator")
    print("="*50)

def main():
    """Main calculator loop."""
    calc = Calculator()
    print_menu()
    
    while True:
        try:
            user_input = input("\nEnter calculation: ").strip().lower()
            
            if user_input in ['quit', 'exit', 'q']:
                print("Thank you for using the calculator!")
                break
            elif user_input == 'help':
                print_menu()
            elif user_input == 'history':
                calc.show_history()
            elif user_input == 'clear':
                calc.clear_history()
            elif user_input == '':
                continue
            else:
                # Evaluate the expression
                result = calc.evaluate_expression(user_input)
                print(f"Result: {result}")
                
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nCalculator interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()