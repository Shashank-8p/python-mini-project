/* ═══════════════════════════════════════════
   ANIMATED SNAKES & LADDERS BOARD ON CANVAS
   Fixed: canvas now fills 100% of hero section
═══════════════════════════════════════════ */
const canvas = document.getElementById('boardCanvas');

if (canvas) {
    const ctx = canvas.getContext('2d');

    /* Force canvas to fill the hero section absolutely */
(function positionCanvas() {
    const hero = canvas.closest('.hero-section') || canvas.parentElement;
    if (hero && getComputedStyle(hero).position === 'static') {
        hero.style.position = 'relative';
    }
    canvas.style.cssText = [
        'position:absolute',
        'top:0', 'left:0', 'right:0', 'bottom:0',
        'width:100%', 'height:100%',
        'z-index:0',
        'pointer-events:none',
        'display:block',
    ].join(';');
})();

function resize() {
    canvas.width  = canvas.offsetWidth  * devicePixelRatio;
    canvas.height = canvas.offsetHeight * devicePixelRatio;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(devicePixelRatio, devicePixelRatio);
}
resize();
window.addEventListener('resize', resize);

const W = () => canvas.offsetWidth;
const H = () => canvas.offsetHeight;

/* ── Colour palette (pastel greens) ── */
const C = {
    boardLight: '#fff5e6',
    boardDark:  '#f6ead7',
    gridLine:   'rgba(132,97,67,0.12)',
    snakeBody:  '#f08a6a',
    snakeHead:  '#d46c4f',
    ladderRail: '#d19a55',
    ladderRung: '#f0c47c',
    dice:       'rgba(255,255,255,0.88)',
    diceDot:    '#6abf8d',
    token1:     '#6abf8d',
    token2:     '#c7a36b',
    num:        'rgba(132,97,67,0.45)',
};

/* ── Board geometry ── */
const ROWS = 10, COLS = 10;

function cellRect(col, row) {
    const w = W(), h = H();
    const cw = w / COLS, ch = h / ROWS;
    return { x: col * cw, y: (ROWS - 1 - row) * ch, w: cw, h: ch };
}

function cellCenter(n) {
    const idx = n - 1;
    const row = Math.floor(idx / COLS);
    let col = idx % COLS;
    if (row % 2 === 1) col = COLS - 1 - col;
    const r = cellRect(col, row);
    return { x: r.x + r.w / 2, y: r.y + r.h / 2 };
}

/* ── Snakes & Ladders definitions ── */
const snakes  = [[97,78],[95,56],[88,24],[76,37],[74,53],[62,19],[54,34],[19,7]];
const ladders = [[4,25],[9,31],[20,41],[28,84],[40,59],[51,67],[63,81],[71,91]];

/* ── Animated tokens ── */
class Token {
    constructor(color, speed) {
        this.cell  = 1 + Math.floor(Math.random() * 100);
        this.color = color;
        this.speed = speed;
        this.wait  = Math.random() * 200;
        this.r     = 0;
        const c = cellCenter(this.cell);
        this.x = c.x; this.y = c.y;
        this.tx = c.x; this.ty = c.y;
    }
    update() {
        if (this.wait > 0) { this.wait--; return; }
        const dx = this.tx - this.x, dy = this.ty - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 1.5) {
            this.x = this.tx; this.y = this.ty;
            if (Math.random() < 0.015) {
                this.cell = 1 + Math.floor(Math.random() * 100);
                const c = cellCenter(this.cell);
                this.tx = c.x; this.ty = c.y;
                this.wait = 30 + Math.random() * 80;
            }
        } else {
            this.x += dx * this.speed;
            this.y += dy * this.speed;
        }
        this.r += 0.04;
    }
    draw() {
        const s = Math.min(W(), H()) * 0.025;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(Math.sin(this.r) * 0.3);
        ctx.beginPath();
        ctx.arc(0, 0, s, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.restore();
    }
}

const tokens = [
    new Token(C.token1, 0.06),
    new Token(C.token2, 0.05),
];

/* ── Dice animation ── */
const diceAnim = { val: 1, t: 0 };

/* ── Draw board ── */
function drawBoard() {
    const w = W(), h = H();
    ctx.fillStyle = '#fff9f0';
    ctx.fillRect(0, 0, w, h);

    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const r = cellRect(col, row);
            ctx.fillStyle = (row + col) % 2 === 0 ? C.boardLight : C.boardDark;
            ctx.fillRect(r.x, r.y, r.w, r.h);
            ctx.strokeStyle = C.gridLine;
            ctx.lineWidth = 0.5;
            ctx.strokeRect(r.x, r.y, r.w, r.h);

            /* cell numbers */
            const cellNum = (row % 2 === 0)
                ? (row * COLS + col + 1)
                : (row * COLS + (COLS - col));
            ctx.fillStyle = C.num;
            ctx.font = `bold ${Math.max(9, r.w * 0.22)}px Nunito, sans-serif`;
            ctx.textAlign = 'left';
            ctx.textBaseline = 'top';
            ctx.fillText(cellNum, r.x + r.w * 0.08, r.y + r.h * 0.06);
        }
    }
}

/* ── Draw snakes ── */
function drawSnakes() {
    snakes.forEach(([from, to]) => {
        const a = cellCenter(from), b = cellCenter(to);
        const t = performance.now() / 1200;
        const segments = 20;
        const amp = Math.min(W(), H()) * 0.025;

        ctx.beginPath();
        for (let i = 0; i <= segments; i++) {
            const p = i / segments;
            const x = a.x + (b.x - a.x) * p + Math.sin(p * Math.PI * 3 + t) * amp;
            const y = a.y + (b.y - a.y) * p;
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.strokeStyle = C.snakeBody;
        ctx.lineWidth = Math.min(W(), H()) * 0.018;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.globalAlpha = 0.7;
        ctx.stroke();
        ctx.globalAlpha = 1;

        /* head */
        ctx.beginPath();
        ctx.arc(a.x, a.y, Math.min(W(), H()) * 0.016, 0, Math.PI * 2);
        ctx.fillStyle = C.snakeHead;
        ctx.fill();

        /* eyes */
        const eyeR = Math.min(W(), H()) * 0.004;
        ctx.beginPath();
        ctx.arc(a.x - eyeR * 1.8, a.y - eyeR * 1.5, eyeR, 0, Math.PI * 2);
        ctx.arc(a.x + eyeR * 1.8, a.y - eyeR * 1.5, eyeR, 0, Math.PI * 2);
        ctx.fillStyle = '#fff';
        ctx.fill();
    });
}

/* ── Draw ladders ── */
function drawLadders() {
    ladders.forEach(([from, to]) => {
        const a = cellCenter(from), b = cellCenter(to);
        const dx = b.x - a.x, dy = b.y - a.y;
        const len = Math.sqrt(dx * dx + dy * dy);
        const ux = -dy / len, uy = dx / len;
        const rail = Math.min(W(), H()) * 0.012;

        [rail, -rail].forEach(off => {
            ctx.beginPath();
            ctx.moveTo(a.x + ux * off, a.y + uy * off);
            ctx.lineTo(b.x + ux * off, b.y + uy * off);
            ctx.strokeStyle = C.ladderRail;
            ctx.lineWidth = Math.min(W(), H()) * 0.006;
            ctx.globalAlpha = 0.75;
            ctx.stroke();
            ctx.globalAlpha = 1;
        });

        const rungs = Math.round(len / (Math.min(W(), H()) * 0.065));
        for (let i = 1; i < rungs; i++) {
            const p = i / rungs;
            const rx = a.x + dx * p, ry = a.y + dy * p;
            ctx.beginPath();
            ctx.moveTo(rx + ux * rail, ry + uy * rail);
            ctx.lineTo(rx - ux * rail, ry - uy * rail);
            ctx.strokeStyle = C.ladderRung;
            ctx.lineWidth = Math.min(W(), H()) * 0.005;
            ctx.globalAlpha = 0.7;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }
    });
}

/* ── Draw animated dice ── */
function roundRect(cx, x, y, w, h, r) {
    cx.beginPath();
    cx.moveTo(x + r, y);
    cx.lineTo(x + w - r, y); cx.arcTo(x + w, y, x + w, y + r, r);
    cx.lineTo(x + w, y + h - r); cx.arcTo(x + w, y + h, x + w - r, y + h, r);
    cx.lineTo(x + r, y + h); cx.arcTo(x, y + h, x, y + h - r, r);
    cx.lineTo(x, y + r); cx.arcTo(x, y, x + r, y, r);
    cx.closePath();
}

function diceDots(v) {
    return {
        1: [[0, 0]],
        2: [[-1,-1],[1,1]],
        3: [[-1,-1],[0,0],[1,1]],
        4: [[-1,-1],[1,-1],[-1,1],[1,1]],
        5: [[-1,-1],[1,-1],[0,0],[-1,1],[1,1]],
        6: [[-1,-1],[1,-1],[-1,0],[1,0],[-1,1],[1,1]],
    }[v] || [];
}

function drawDice() {
    const w = W(), h = H();
    const size = Math.min(w, h) * 0.055;
    const px = w * 0.06, py = h * 0.12;

    diceAnim.t += 0.03;
    if (Math.random() < 0.01) diceAnim.val = 1 + Math.floor(Math.random() * 6);

    ctx.save();
    ctx.translate(px, py);
    ctx.rotate(Math.sin(diceAnim.t * 0.7) * 0.2);

    ctx.fillStyle = C.dice;
    ctx.shadowColor = 'rgba(30,138,88,0.3)';
    ctx.shadowBlur = 12;
    roundRect(ctx, -size / 2, -size / 2, size, size, size * 0.18);
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.fillStyle = C.diceDot;
    const dr = size * 0.09;
    diceDots(diceAnim.val).forEach(([ddx, ddy]) => {
        ctx.beginPath();
        ctx.arc(ddx * size * 0.3, ddy * size * 0.3, dr, 0, Math.PI * 2);
        ctx.fill();
    });

    ctx.restore();
}

/* ── Main loop ── */
function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBoard();
    drawLadders();
    drawSnakes();
    tokens.forEach(t => { t.update(); t.draw(); });
    drawDice();
    requestAnimationFrame(loop);
    }

    loop();
}
