const API_BASE = "https://smart-interview-backend.onrender.com";

let totalQuestions = 0;
let currentQuestionIndex = 0;

let sessionScores = [];
let sessionDifficulties = [];

let currentQuestionId = null;
let currentDifficulty = null;

let timerInterval;
let timeRemaining = 60;

async function getQuestion() {

    if (currentQuestionIndex === 0) {
        totalQuestions = parseInt(document.getElementById("questionLimit").value);

        sessionScores = [];
        sessionDifficulties = [];

        document.getElementById("questionLimit").disabled = true;
        document.getElementById("difficulty").disabled = true;
    }

    if (currentQuestionIndex >= totalQuestions) {
        showSummary();
        return;
    }

    clearInterval(timerInterval);

    const domain = document.getElementById("domain").value;

    const response = await fetch(`${API_BASE}/question/${domain}`);
    const data = await response.json();

    currentQuestionId = data.id;
    currentDifficulty = data.difficulty;

    document.getElementById("questionBox").innerText = data.question_text;
    document.getElementById("answer").value = "";
    document.getElementById("result").innerText = "";

    currentQuestionIndex++;
    updateProgress();
    startTimer();
}

async function submitAnswer() {

    const answer = document.getElementById("answer").value.trim();

    if (answer === "") {
        alert("Please write an answer before submitting.");
        return;
    }

    clearInterval(timerInterval);

    const response = await fetch(`${API_BASE}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            question_id: currentQuestionId,
            user_answer: answer
        })
    });

    const data = await response.json();

    sessionScores.push(data.score);
    sessionDifficulties.push(currentDifficulty);

    document.getElementById("result").innerText =
        `Score: ${data.score} / 10`;

    setTimeout(() => {
        getQuestion();
    }, 1500);
}

function updateProgress() {

    let percent = (currentQuestionIndex / totalQuestions) * 100;

    document.getElementById("progressBar").style.width = percent + "%";

    document.getElementById("progressText").innerText =
        `Question ${currentQuestionIndex} of ${totalQuestions}`;
}

function startTimer() {

    timeRemaining = 60;

    document.getElementById("timerDisplay").innerText =
        `Time Left: ${timeRemaining}s`;

    timerInterval = setInterval(() => {

        timeRemaining--;

        document.getElementById("timerDisplay").innerText =
            `Time Left: ${timeRemaining}s`;

        if (timeRemaining <= 10) {
            document.getElementById("timerDisplay").style.color = "red";
        } else {
            document.getElementById("timerDisplay").style.color = "black";
        }

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            alert("Time's up!");
            getQuestion();
        }

    }, 1000);
}

function showSummary() {

    clearInterval(timerInterval);

    document.getElementById("sessionSummary").style.display = "block";

    document.getElementById("questionLimit").disabled = false;
    document.getElementById("difficulty").disabled = false;

    const total = sessionScores.reduce((a, b) => a + b, 0);
    const average = total / sessionScores.length;

    let breakdown = {
        Easy: [],
        Medium: [],
        Hard: []
    };

    for (let i = 0; i < sessionScores.length; i++) {
        breakdown[sessionDifficulties[i]].push(sessionScores[i]);
    }

    let breakdownHTML = `
        <p><strong>Overall Average:</strong> ${average.toFixed(2)} / 10</p>
    `;

    for (let level in breakdown) {
        if (breakdown[level].length > 0) {
            let avg =
                breakdown[level].reduce((a, b) => a + b, 0) /
                breakdown[level].length;

            breakdownHTML += `
                <p>${level}: ${avg.toFixed(2)} / 10</p>
            `;
        }
    }

    document.getElementById("finalScore").innerHTML = breakdownHTML;

    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
    });
}

function restartSession() {

    currentQuestionIndex = 0;
    sessionScores = [];
    sessionDifficulties = [];

    clearInterval(timerInterval);

    document.getElementById("progressBar").style.width = "0%";
    document.getElementById("progressText").innerText = "";
    document.getElementById("sessionSummary").style.display = "none";
    document.getElementById("result").innerText = "";
    document.getElementById("questionBox").innerText =
        "Click Get Question to begin.";
    document.getElementById("timerDisplay").innerText = "";
}

async function loadAnalytics() {

    const response = await fetch(`${API_BASE}/analytics`);
    const data = await response.json();

    document.getElementById("total").innerText = data.total_attempts;
    document.getElementById("average").innerText =
        data.average_score.toFixed(2);

    // ===== Domain Chart =====
    const domains = Object.keys(data.domain_performance);
    const scores = Object.values(data.domain_performance);

    const ctx1 = document.getElementById("domainChart");

    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: domains,
            datasets: [{
                label: 'Average Score by Domain',
                data: scores,
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    // ===== Difficulty Chart (Session Only) =====
    if (typeof sessionDifficulties !== "undefined" &&
        sessionDifficulties.length > 0) {

        let difficultyData = {
            Easy: 0,
            Medium: 0,
            Hard: 0
        };

        for (let i = 0; i < sessionScores.length; i++) {
            difficultyData[sessionDifficulties[i]] += sessionScores[i];
        }

        const ctx2 = document.getElementById("difficultyChart");

        new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: Object.keys(difficultyData),
                datasets: [{
                    data: Object.values(difficultyData),
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545'
                    ]
                }]
            }
        });
    }
}
