function getFlappyGameHTML() {
    return `
        <div class="project-content">
            <h2>🐦 Flappy Bird</h2>

            <div id="flappyStartScreen" class="flappy-start-screen">
                <div class="flappy-instructions">
                    <h3>🎮 How to Play</h3>
                    <ul>
                        <li>Press <strong>SPACE</strong> or <strong>click</strong> to jump.</li>
                        <li>Avoid the green pipes.</li>
                        <li>Stay inside the game screen.</li>
                    </ul>
                </div>

                <button id="flappyStartBtn" class="flappy-btn-action">▶️ Start Playing</button>
            </div>

            <div id="flappyGameScreen" class="flappy-container" style="display: none;">
                <div id="flappy-canvas-wrapper">
                    <canvas id="flappyCanvas" width="400" height="600"></canvas>
                </div>

                <div class="flappy-controls">
                    <button id="flappyBackBtn" class="flappy-btn-action flappy-btn-secondary">🔙 Back to Menu</button>
                </div>
            </div>
        </div>

        <style>
            .flappy-start-screen {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 2rem;
                padding: 2rem;
                background: var(--surface-color, #ffffff);
                border-radius: 12px;
                border: 1px solid var(--border-color, #e5e7eb);
                margin: 1rem auto;
                max-width: 500px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }

            .flappy-instructions {
                width: 100%;
                color: var(--text-color, #111827);
            }

            .flappy-instructions h3 {
                color: var(--primary-color, #4f46e5);
                margin-bottom: 1rem;
                border-bottom: 2px solid var(--border-color, #e5e7eb);
                padding-bottom: 0.5rem;
            }

            .flappy-instructions ul {
                margin-bottom: 1.5rem;
                padding-left: 1.5rem;
            }

            .flappy-instructions li {
                margin-bottom: 0.5rem;
                line-height: 1.5;
            }

            .flappy-btn-action {
                font-size: 1.1rem;
                padding: 0.9rem 2rem;
                background: var(--primary-color, #4f46e5);
                color: white;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                font-weight: bold;
            }

            .flappy-btn-secondary {
                background: var(--surface-color, #ffffff);
                border: 2px solid var(--border-color, #e5e7eb);
                color: var(--text-color, #111827);
                margin-top: 1rem;
            }

            .flappy-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 10px;
                gap: 1rem;
            }

            #flappy-canvas-wrapper {
                position: relative;
                border: 3px solid var(--border-color);
                background: #0f172a; /* Sleek dark slate background */
                overflow: hidden;
                width: 100%;
                max-width: 400px;
                aspect-ratio: 1 / 1;
                border-radius: 8px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                touch-action: none;
            }

            #flappyCanvas {
                display: block;
                cursor: pointer;
                width: 100%;
                height: 100%;
            }
        </style>
    `;
}

function initFlappyGame() {
    const startScreen = document.getElementById("flappyStartScreen");
    const gameScreen = document.getElementById("flappyGameScreen");
    const startBtn = document.getElementById("flappyStartBtn");
    const backBtn = document.getElementById("flappyBackBtn");
    const canvas = document.getElementById("flappyCanvas");

    if (!startScreen || !gameScreen || !startBtn || !backBtn || !canvas) {
        console.warn("Flappy Bird elements not found.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;

    const SKY_BLUE = "#87ceeb";
    const GREEN = "#00c800";
    const DARK_GREEN = "#009600";
    const YELLOW = "#ffdc00";
    const WHITE = "#ffffff";
    const BLACK = "#000000";

    const bird = {
        x: 80,
        y: HEIGHT / 2,
        radius: 15,
        velocity: 0,
        gravity: 0.35,
        jumpStrength: -7
    };

    const pipeWidth = 60;
    const pipeGap = 180;
    const pipeSpeed = 2;

    let pipes = [];
    let score = 0;
    let gameRunning = false;
    let animationId = null;

    function createPipe() {
        const gapY = Math.floor(Math.random() * ((HEIGHT - 200) - 150 + 1)) + 150;
        pipes.push({ x: WIDTH, gapY: gapY, passed: false });
    }

    function drawBird() {
        // Yellow body
        ctx.fillStyle = YELLOW;
        ctx.beginPath();
        ctx.arc(bird.x, bird.y, bird.radius, 0, Math.PI * 2);
        ctx.fill();

        // Black eye
        ctx.fillStyle = BLACK;
        ctx.beginPath();
        ctx.arc(bird.x + 6, bird.y - 5, 3, 0, Math.PI * 2);
        ctx.fill();

        // Black beak
        ctx.fillStyle = BLACK;
    ctx.beginPath();
    ctx.moveTo(bird.x + bird.radius + 5, bird.y);      // tip of beak
    ctx.lineTo(bird.x + bird.radius, bird.y - 6);       // upper base
    ctx.lineTo(bird.x + bird.radius, bird.y + 6);       // lower base\
    ctx.closePath();
    ctx.fill();
    }

    function drawPipes() {
        pipes.forEach(pipe => {
            const bottomY = pipe.gapY + pipeGap;

            ctx.fillStyle = GREEN;
            ctx.fillRect(pipe.x, 0, pipeWidth, pipe.gapY);
            ctx.fillRect(pipe.x, bottomY, pipeWidth, HEIGHT - bottomY);

            ctx.fillStyle = DARK_GREEN;
            ctx.fillRect(pipe.x, pipe.gapY - 20, pipeWidth, 20);
            ctx.fillRect(pipe.x, bottomY, pipeWidth, 20);
        });
    }

    function checkCollision() {
        if (bird.y - bird.radius <= 0 || bird.y + bird.radius >= HEIGHT) {
            return true;
        }

        for (const pipe of pipes) {
            const birdLeft = bird.x - bird.radius;
            const birdRight = bird.x + bird.radius;
            const birdTop = bird.y - bird.radius;
            const birdBottom = bird.y + bird.radius;

            const pipeLeft = pipe.x;
            const pipeRight = pipe.x + pipeWidth;
            const topPipeBottom = pipe.gapY;
            const bottomPipeTop = pipe.gapY + pipeGap;

            const insidePipeX = birdRight > pipeLeft && birdLeft < pipeRight;
            const hitTopPipe = birdTop < topPipeBottom;
            const hitBottomPipe = birdBottom > bottomPipeTop;

            if (insidePipeX && (hitTopPipe || hitBottomPipe)) {
                return true;
            }
        }

        return false;
    }

    function drawScore() {
        ctx.fillStyle = WHITE;
        ctx.font = "32px Arial";
        ctx.textAlign = "left";
        ctx.fillText(`Score: ${score}`, 10, 40);
    }

    function gameOverScreen() {
        ctx.fillStyle = SKY_BLUE;
        ctx.fillRect(0, 0, WIDTH, HEIGHT);

        ctx.fillStyle = BLACK;
        ctx.textAlign = "center";

        ctx.font = "40px Arial";
        ctx.fillText("Game Over!", WIDTH / 2, 220);

        ctx.font = "36px Arial";
        ctx.fillText(`Score: ${score}`, WIDTH / 2, 270);

        ctx.font = "22px Arial";
        ctx.fillText("Press SPACE or Click to Restart", WIDTH / 2, 340);
    }

    function resetGame() {
        bird.y = HEIGHT / 2;
        bird.velocity = 0;
        pipes = [];
        score = 0;
        gameRunning = true;
        createPipe();
    }

    function update() {
        if (!gameRunning) return;

        bird.velocity += bird.gravity;
        bird.y += bird.velocity;

        pipes.forEach(pipe => {
            pipe.x -= pipeSpeed;
        });

        if (pipes.length === 0 || pipes[pipes.length - 1].x < WIDTH - 220) {
            createPipe();
        }

        pipes = pipes.filter(pipe => pipe.x + pipeWidth > 0);

        pipes.forEach(pipe => {
            if (!pipe.passed && pipe.x + pipeWidth < bird.x) {
                score++;
                pipe.passed = true;
            }
        });

        if (checkCollision()) {
            gameRunning = false;
        }
    }

    function draw() {
        if (gameRunning) {
            ctx.fillStyle = SKY_BLUE;
            ctx.fillRect(0, 0, WIDTH, HEIGHT);
            drawBird();
            drawPipes();
            drawScore();
        } else {
            gameOverScreen();
        }
    }

    function gameLoop() {
        update();
        draw();
        animationId = requestAnimationFrame(gameLoop);
    }

    function startGame() {
        if (animationId) {
            cancelAnimationFrame(animationId);
        }

        resetGame();
        gameLoop();
    }

    function tap(e) {
        if (e && e.preventDefault) {
            e.preventDefault();
        }

        jump();
    }
    function jump() {
        if (!gameRunning) {
            startGame();
        }

        bird.velocity = bird.jumpStrength;
    }

    function handleKeyDown(event) {
        if (gameScreen.style.display === "none") return;

        if (event.code === "Space") {
            event.preventDefault();
            jump();
        }
    }

    canvas.addEventListener('mousedown', tap);
    canvas.addEventListener('touchstart', tap, { passive: false });


    function stopGame() {
        if (animationId) {
            cancelAnimationFrame(animationId);
            animationId = null;
        }
        gameRunning = false;
    }

    console.log(startBtn);
    startBtn.addEventListener("click", function () {
        startScreen.style.display = "none";
        gameScreen.style.display = "flex";
        startGame();
    });

    backBtn.addEventListener("click", function () {
        stopGame();
        gameScreen.style.display = "none";
        startScreen.style.display = "flex";
    });

    canvas.addEventListener("click", jump);
    document.addEventListener("keydown", handleKeyDown);
}