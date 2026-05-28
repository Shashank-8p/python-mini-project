function getProductivePetHTML() {
    return `
        <div class="productive-pet-container">
            <h2 class="pet-title">🐱 Productive Pet</h2>

            <div class="pet-card">
                <div id="petLevel">Level 1</div>

                <div class="pet-emoji">🐱</div>

                <div id="petMood">Tired 🥱</div>

                <div class="xp-bar">
                    <div class="xp-fill"></div>
                </div>

                <span id="xpText">0 / 100 XP</span>

                <div class="task-input-area">
                    <input id="taskInput" placeholder="Enter task..." />
                    <button id="addTaskBtn">Add Task</button>
                </div>

                <ul id="taskList"></ul>

                <div id="streakText">🔥 Streak: 0</div>
            </div>
        </div>
    `;
}
function initProductivePet() {

    setTimeout(() => {

        let xp = 0;
        let level = 1;
        let streak = 0;

        const addTaskBtn = document.getElementById("addTaskBtn");
        const taskInput = document.getElementById("taskInput");
        const xpFill = document.querySelector(".xp-fill");
        const xpText = document.getElementById("xpText");
        const petMood = document.getElementById("petMood");
        const petEmoji = document.querySelector(".pet-emoji");
        const taskList = document.getElementById("taskList");
        const levelText = document.getElementById("petLevel");
        const streakText = document.getElementById("streakText");

        if (!addTaskBtn || !taskInput) return;

        function getPetState(level) {
            if (level >= 10) return { emoji: "🐉", mood: "Mythic Beast 🔥" };
            if (level >= 7) return { emoji: "🐯", mood: "Legend Pet 👑" };
            if (level >= 5) return { emoji: "🦁", mood: "Alpha Pet 😎" };
            if (level >= 3) return { emoji: "😸", mood: "Super Happy 🎉" };
            return { emoji: "🐱", mood: "Happy 😊" };
        }

        function updatePetUI() {
            xpFill.style.width = `${xp}%`;
            xpText.innerText = `${xp} / 100 XP`;
            levelText.innerText = `Level ${level}`;
            streakText.innerText = `🔥 Streak: ${streak}`;

            const petState = getPetState(level);

            petMood.innerText = petState.mood;
            petEmoji.innerText = petState.emoji;
        }

        addTaskBtn.addEventListener("click", () => {

            const task = taskInput.value.trim();
            if (!task) return alert("Please enter a task!");

            const li = document.createElement("li");
            li.innerHTML = `
                <span>${task}</span>
                <button class="complete-btn">Complete</button>
            `;

            taskList.appendChild(li);
            taskInput.value = "";

            const completeBtn = li.querySelector(".complete-btn");

            completeBtn.addEventListener("click", () => {

                if (completeBtn.disabled) return;

                xp += 20;
                streak += 1;

                if (streak % 5 === 0) xp += 10;

                while (xp >= 100) {
                    level++;
                    xp -= 100;
                }

                li.style.opacity = "0.6";
                li.style.textDecoration = "line-through";

                completeBtn.innerText = "Done ✓";
                completeBtn.disabled = true;

                updatePetUI();
            });
        });

        updatePetUI();

    }, 0);
}