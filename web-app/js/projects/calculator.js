function getCalculatorHTML() {
    return `
    <div class="project-content">
        <h2>🧮 Ultra Pro Calculator</h2>

        <div class="calculator">
            <div class="calc-display" id="calcDisplay">0</div>

            <div class="calc-buttons">

                <!-- TOP ROW -->
                <button class="calc-btn clear" data-action="clear">C</button>
                <button class="calc-btn operator" data-action="delete">⌫</button>
                <button class="calc-btn operator" data-action="(">(</button>
                <button class="calc-btn operator" data-action=")">)</button>

                <!-- SCIENTIFIC -->
                <button class="calc-btn operator" data-action="sin">sin</button>
                <button class="calc-btn operator" data-action="cos">cos</button>
                <button class="calc-btn operator" data-action="tan">tan</button>
                <button class="calc-btn operator" data-action="sqrt">√</button>

                <button class="calc-btn operator" data-action="square">x²</button>
                <button class="calc-btn operator" data-action="inv">1/x</button>
                <button class="calc-btn operator" data-action="^">xʸ</button>
                <button class="calc-btn operator" data-action="/">÷</button>

                <!-- NUMBERS -->
                <button class="calc-btn number" data-value="7">7</button>
                <button class="calc-btn number" data-value="8">8</button>
                <button class="calc-btn number" data-value="9">9</button>
                <button class="calc-btn operator" data-action="*">×</button>

                <button class="calc-btn number" data-value="4">4</button>
                <button class="calc-btn number" data-value="5">5</button>
                <button class="calc-btn number" data-value="6">6</button>
                <button class="calc-btn operator" data-action="-">−</button>

                <button class="calc-btn number" data-value="1">1</button>
                <button class="calc-btn number" data-value="2">2</button>
                <button class="calc-btn number" data-value="3">3</button>
                <button class="calc-btn operator" data-action="+">+</button>

                <button class="calc-btn number span-2" data-value="0">0</button>
                <button class="calc-btn number" data-value=".">.</button>
                <button class="calc-btn equals" data-action="=">=</button>

            </div>
        </div>
    </div>

    <style>
        .calculator{
            max-width:380px;
            margin:2rem auto;
            padding:1.2rem;
            background:var(--surface-color);
            border-radius:22px;
            box-shadow:var(--shadow);
        }

        .calc-display{
            background:var(--bg-color);
            padding:1.5rem;
            border-radius:16px;
            font-size:2.2rem;
            text-align:right;
            margin-bottom:1rem;
            min-height:70px;
            display:flex;
            align-items:center;
            justify-content:flex-end;
            word-break:break-all;
        }

        .calc-buttons{
            display:grid;
            grid-template-columns:repeat(4,1fr);
            gap:0.6rem;
        }

        .calc-btn{
            padding:1rem;
            font-size:1.1rem;
            border:none;
            border-radius:12px;
            cursor:pointer;
            font-weight:600;
            transition:0.2s;
        }

        .calc-btn:hover{
            transform:scale(1.05);
        }

        .number{
            background:var(--surface-color);
            border:2px solid var(--border-color);
            color:var(--text-color);
        }

        .operator{
            background:var(--primary-color);
            color:white;
        }

        .equals{
            background:var(--success-color);
            color:white;
        }

        .clear{
            background:var(--danger-color);
            color:white;
        }

        .span-2{
            grid-column:span 2;
        }
    </style>
    `;
}

function initCalculator() {
    const display = document.getElementById("calcDisplay");
    if (!display) return;

    let expression = "";

    function update() {
        display.textContent = expression || "0";
    }

    function format(expr) {
        return expr
            .replace(/÷/g, "/")
            .replace(/×/g, "*")
            .replace(/\^/g, "**");
    }

    function safeEval(expr) {
        try {
            return String(eval(format(expr)));
        } catch {
            return "Error";
        }
    }

    function applyFunction(type) {
        try {
            let value = eval(format(expression || "0"));

            switch (type) {
                case "sin": return String(Math.sin(value));
                case "cos": return String(Math.cos(value));
                case "tan": return String(Math.tan(value));
                case "sqrt": return String(Math.sqrt(value));
                case "square": return String(value * value);
                case "inv": return value === 0 ? "Error" : String(1 / value);
            }
        } catch {
            return "Error";
        }
    }

    document.querySelectorAll(".calc-btn").forEach(btn => {
        btn.addEventListener("click", () => {

            const value = btn.dataset.value;
            const action = btn.dataset.action;

            if (value !== undefined) {
                expression += value;
                update();
                return;
            }

            if (!action) return;

            switch (action) {

                case "clear":
                    expression = "";
                    break;

                case "delete":
                    expression = expression.slice(0, -1);
                    break;

                case "=":
                    expression = safeEval(expression);
                    break;

                case "sin":
                case "cos":
                case "tan":
                case "sqrt":
                case "square":
                case "inv":
                    expression = applyFunction(action);
                    break;

                case "^":
                    expression += "^";
                    break;

                default:
                    expression += action;
            }

            update();
        });
    });

    document.addEventListener("keydown", (e) => {

        if (!isNaN(e.key) || e.key === ".") expression += e.key;

        if (["+", "-", "*", "/"].includes(e.key)) expression += e.key;

        if (e.key === "^") expression += "^";

        if (e.key === "Enter") expression = safeEval(expression);

        if (e.key === "Backspace") expression = expression.slice(0, -1);

        update();
    });

    update();
}
