function getCalculatorHTML() {
    return `
        <div class="project-content">
            <h2>🧮 Calculator</h2>
            <div class="calculator">
                <div class="calc-display" id="calcDisplay">0</div>
                <div class="calc-buttons">
                    <button class="calc-btn clear" data-action="clear">C</button>
                    <button class="calc-btn operator" data-action="delete">⌫</button>
                    <button class="calc-btn operator" data-action="/">/</button>
                    <button class="calc-btn operator" data-action="*">×</button>
                    
                    <button class="calc-btn number" data-value="7">7</button>
                    <button class="calc-btn number" data-value="8">8</button>
                    <button class="calc-btn number" data-value="9">9</button>
                    <button class="calc-btn operator" data-action="-">−</button>
                    
                    <button class="calc-btn number" data-value="4">4</button>
                    <button class="calc-btn number" data-value="5">5</button>
                    <button class="calc-btn number" data-value="6">6</button>
                    <button class="calc-btn operator" data-action="+">+</button>
                    
                    <button class="calc-btn number" data-value="1">1</button>
                    <button class="calc-btn number" data-value="2">2</button>
                    <button class="calc-btn number" data-value="3">3</button>
                    <button class="calc-btn operator" data-action="**">^</button>
                    
                    <button class="calc-btn number span-2" data-value="0">0</button>
                    <button class="calc-btn number" data-value=".">.</button>
                    <button class="calc-btn equals" data-action="=">=</button>
                </div>
            </div>
        </div>
        
        <style>
            .calculator {
                max-width: 350px;
                margin: 2rem auto;
                background: var(--surface-color);
                padding: 1.5rem;
                border-radius: 20px;
                box-shadow: var(--shadow);
            }
            
            .calc-display {
                background: var(--bg-color);
                padding: 2rem;
                border-radius: 15px;
                font-size: 2.5rem;
                text-align: right;
                margin-bottom: 1rem;
                min-height: 80px;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                word-break: break-all;
            }
            
            .calc-buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 0.75rem;
            }
            
            .calc-btn {
                padding: 1.5rem;
                font-size: 1.5rem;
                border: none;
                border-radius: 15px;
                cursor: pointer;
                transition: var(--transition);
                font-weight: 600;
            }
            
            .calc-btn.number {
                background: var(--surface-color);
                border: 2px solid var(--border-color);
                color: var(--text-color);
            }
            
            .calc-btn.operator {
                background: var(--primary-color);
                color: white;
            }
            
            .calc-btn.equals {
                background: var(--success-color);
                color: white;
            }
            
            .calc-btn.clear {
                background: var(--danger-color);
                color: white;
            }
            
            .calc-btn:hover {
                transform: scale(1.05);
            }
            
            .calc-btn.span-2 {
                grid-column: span 2;
            }
        </style>
    `;
}

function initCalculator() {
    const display = document.getElementById('calcDisplay');
    let currentValue = '0';
    let previousValue = '';
    let operation = '';
    let isNewOperand = false; 
    
    document.querySelectorAll('.calc-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const value = btn.getAttribute('data-value');
            const action = btn.getAttribute('data-action');
            
            if (value) {
                handleNumber(value);
            } else if (action) {
                handleAction(action);
            }
            
            updateDisplay();
        });
    });
    
    function handleNumber(num) {
        // Prevent multiple decimals
        if (num === '.' && currentValue.includes('.')) return;
        
        if (currentValue === '0' || currentValue === 'Error' || isNewOperand) {
            // Start fresh if it's a new operand or clearing a zero/error
            currentValue = num === '.' ? '0.' : num;
            isNewOperand = false;
        } else {
            currentValue += num;
        }
    }
    
    function handleAction(action) {
        if (action === 'clear') {
            currentValue = '0';
            previousValue = '';
            operation = '';
        } else if (action === 'delete') {
            if (!isNewOperand && currentValue !== 'Error') {
                currentValue = currentValue.slice(0, -1) || '0';
            }
        } else if (action === '=') {
            if (operation && previousValue) {
                calculate();
                operation = ''; // Clear operation after equals
            }
        } else {
            // If the user clicks an operator but hasn't typed a new number yet, 
            // just swap the operator instead of calculating.
            if (operation && previousValue && !isNewOperand) {
                calculate();
            }
            previousValue = currentValue;
            operation = action;
            isNewOperand = true; // Ready for the next number
        }
    }
    
    function calculate() {
        const prev = parseFloat(previousValue);
        const curr = parseFloat(currentValue);
        let result;
        
        if (isNaN(prev) || isNaN(curr)) return;
        
        switch (operation) {
            case '+': result = prev + curr; break;
            case '-': result = prev - curr; break;
            case '*': result = prev * curr; break;
            case '/': 
                if (curr === 0) {
                    currentValue = 'Error';
                    previousValue = '';
                    return;
                }
                result = prev / curr; 
                break;
            case '**': result = Math.pow(prev, curr); break;
            default: return;
        }
        
        // Fix JS floating point precision issues (e.g., 0.1 + 0.2)
        result = parseFloat(result.toPrecision(12));
        
        currentValue = result.toString();
        previousValue = '';
    }
    
    function updateDisplay() {
        display.textContent = currentValue;
    }
}