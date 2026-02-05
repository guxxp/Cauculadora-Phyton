class Calculator {
    constructor() {
        this.currentDisplay = document.getElementById('currentDisplay');
        this.prevExpression = document.getElementById('prevExpression');
        this.expression = '';
        this.init();
    }

    init() {
        // Number buttons
        document.querySelectorAll('.btn-number').forEach(btn => {
            btn.addEventListener('click', () => {
                const value = btn.dataset.value;
                this.handleNumber(value);
            });
        });

        // Operator buttons
        document.querySelectorAll('.btn-operator').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleOperator(action);
            });
        });

        // Function buttons
        document.querySelectorAll('.btn-function').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleFunction(action);
            });
        });

        // Keyboard support
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    handleNumber(value) {

        if (this.expression === '0' && value !== '.') {
            this.expression = value;
        } else {
            this.expression += value;
        }
        this.updateDisplay();
    }

    handleOperator(action) {
        switch (action) {
            case 'add':
                this.expression += '+';
                break;
            case 'subtract':
                this.expression += '-';
                break;
            case 'multiply':
                this.expression += '×';
                break;
            case 'divide':
                this.expression += '÷';
                break;
            case 'equals':
                this.calculate();
                return;
        }
        this.updateDisplay();
    }

    handleFunction(action) {
        switch (action) {
            case 'clear':
                this.clear();
                break;
            case 'toggle-sign':
                this.toggleSign();
                break;
            case 'percent':
                this.percent();
                break;
        }
    }

    clear() {
        this.expression = '';
        this.prevExpression.textContent = '';
        this.currentDisplay.textContent = '0';
    }

    toggleSign() {
        if (this.expression) {
            if (this.expression.startsWith('-')) {
                this.expression = this.expression.slice(1);
            } else {
                this.expression = '-' + this.expression;
            }
            this.updateDisplay();
        }
    }

    percent() {
        if (this.expression) {
            try {
                const calcExpr = this.expression.replace(/×/g, '*').replace(/÷/g, '/');
                const result = eval(calcExpr) / 100;
                this.expression = String(result);
                this.updateDisplay();
            } catch (error) {
                this.showError();
            }
        }
    }

    calculate() {
        if (!this.expression) return;

        try {
            // Replace visual operators with JavaScript operators
            const calcExpr = this.expression.replace(/×/g, '*').replace(/÷/g, '/');

            // Validate expression (only allow numbers and basic operators)
            if (!/^[\d+\-*/.() ]+$/.test(calcExpr)) {
                this.showError();
                return;
            }

            const result = eval(calcExpr);

            // Check for division by zero or invalid result
            if (!isFinite(result)) {
                this.currentDisplay.textContent = 'Div by 0';
                this.expression = '';
                return;
            }

            // Format result: remove .0 if it's an integer
            const formattedResult = Number.isInteger(result) ? result : result;

            this.prevExpression.textContent = this.expression + ' =';
            this.expression = String(formattedResult);
            this.updateDisplay();
        } catch (error) {
            this.showError();
        }
    }

    showError() {
        this.currentDisplay.textContent = 'Error';
        this.expression = '';
        setTimeout(() => {
            if (this.currentDisplay.textContent === 'Error') {
                this.currentDisplay.textContent = '0';
            }
        }, 1500);
    }

    updateDisplay() {
        this.currentDisplay.textContent = this.expression || '0';
    }

    handleKeyboard(e) {
        // Numbers and operators
        if (/^[0-9.]$/.test(e.key)) {
            this.handleNumber(e.key);
        } else if (e.key === '+') {
            this.handleOperator('add');
        } else if (e.key === '-') {
            this.handleOperator('subtract');
        } else if (e.key === '*') {
            this.handleOperator('multiply');
        } else if (e.key === '/') {
            e.preventDefault();
            this.handleOperator('divide');
        } else if (e.key === 'Enter' || e.key === '=') {
            e.preventDefault();
            this.handleOperator('equals');
        } else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') {
            this.handleFunction('clear');
        } else if (e.key === '%') {
            this.handleFunction('percent');
        } else if (e.key === 'Backspace') {
            this.expression = this.expression.slice(0, -1);
            this.updateDisplay();
        }
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Calculator();
});
