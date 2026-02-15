console.log("SCRIPT LOADED");

const API_BASE = "https://smart-interview-backend.onrender.com";

let totalQuestions = 0;
let currentQuestionIndex = 0;
let sessionScores = [];
let sessionDifficulties = [];
let currentQuestionId = null;
let currentDifficulty = null;
let timerInterval;
let timeRemaining = 60;

let domainChartInstance = null;
let difficultyChartInstance = null;


// coding flow
async function getQuestion() {

    const questionLimitEl = document.getElementById("questionLimit");
    const domainEl = document.getElementById("domain");
    const questionBox = document.getElementById("questionBox");

    if (!questionLimitEl || !domainEl || !questionBox) return;

    if (currentQuestionIndex === 0) {
        totalQuestions = parseInt(questionLimitEl.value);
        sessionScores = [];
        sessionDifficulties = [];
        questionLimitEl.disabled = true;
    }

    if (currentQuestionIndex >= totalQuestions) {
        showSummary();
        return;
    }

    clearInterval(timerInterval);

    const domain = domainEl.value;

    const response = await fetch(`${API_BASE}/question/${domain}`);
    const data = await response.json();

    if (!data || data.error) return;

    currentQuestionId = data.id;
    currentDifficulty = data.difficulty;

    questionBox.innerText = data.question_text;

    const answerEl = document.getElementById("answer");
    const resultEl = document.getElementById("result");

    if (answerEl) answerEl.value = "";
    if (resultEl) resultEl.innerText = "";

    currentQuestionIndex++;
    updateProgress();
    startTimer();
}


async function submitAnswer() {

    const answerEl = document.getElementById("answer");
    const resultEl = document.getElementById("result");

    if (!answerEl || !resultEl) return;

    const answer = answerEl.value.trim();
    if (!answer) return;

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

    resultEl.innerText = `Score: ${data.score} / 100`;

    setTimeout(() => getQuestion(), 1500);
}


function updateProgress() {

    const bar = document.getElementById("progressBar");
    const text = document.getElementById("progressText");

    if (!bar || !text) return;

    let percent = (currentQuestionIndex / totalQuestions) * 100;
    bar.style.width = percent + "%";
    text.innerText = `Question ${currentQuestionIndex} of ${totalQuestions}`;
}


function startTimer() {

    const timerEl = document.getElementById("timerDisplay");
    if (!timerEl) return;

    timeRemaining = 60;
    timerEl.innerText = `Time Left: ${timeRemaining}s`;

    timerInterval = setInterval(() => {

        timeRemaining--;
        timerEl.innerText = `Time Left: ${timeRemaining}s`;

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            getQuestion();
        }

    }, 1000);
}


function showSummary() {

    const summary = document.getElementById("sessionSummary");
    const finalScore = document.getElementById("finalScore");

    if (!summary || !finalScore) return;

    summary.style.display = "block";

    const total = sessionScores.reduce((a, b) => a + b, 0);
    const average = total / sessionScores.length;

    finalScore.innerHTML =
        `<p><strong>Overall Average:</strong> ${average.toFixed(2)} / 100</p>`;
}


function restartSession() {

    currentQuestionIndex = 0;
    sessionScores = [];
    sessionDifficulties = [];

    clearInterval(timerInterval);

    const summary = document.getElementById("sessionSummary");
    if (summary) summary.style.display = "none";
}


// mock interview
async function startMock() {

    const container = document.getElementById("mockContainer");
    if (!container) return;

    const response = await fetch(
        `${API_BASE}/mock-balanced/python`
    );

    const questions = await response.json();
    if (!questions) return;

    container.innerHTML = "";

    questions.forEach((q, index) => {
        container.innerHTML += `
            <div class="card mb-3">
                <div class="card-body">
                    <h5>Question ${index + 1}</h5>
                    <p>${q.question_text}</p>
                </div>
            </div>
        `;
    });
}


// analytics
async function loadAnalytics(category = null) {

    const totalEl = document.getElementById("total");
    const avgEl = document.getElementById("average");
    const chart1 = document.getElementById("domainChart");
    const chart2 = document.getElementById("difficultyChart");

    if (!totalEl || !avgEl || !chart1 || !chart2) return;

    let url = `${API_BASE}/analytics`;
    if (category) url += `?category=${category}`;

    const response = await fetch(url);
    const data = await response.json();

    totalEl.innerText = data.total_attempts;
    avgEl.innerText = data.average_score.toFixed(2);
}


window.onload = function () {
    if (document.getElementById("domainChart")) {
        loadAnalytics("coding");
    }
};
