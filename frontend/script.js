const API_BASE = "https://smart-interview-backend.onrender.com";
let totalQuestions = 0;
let currentQuestionIndex = 0;
let sessionScores = [];

let currentQuestionId = null;

async function getQuestion() {

    if (currentQuestionIndex === 0) {
        totalQuestions = parseInt(document.getElementById("questionLimit").value);
        sessionScores = [];
    }

    if (currentQuestionIndex >= totalQuestions) {
        showSummary();
        return;
    }

    const domain = document.getElementById("domain").value;

    const response = await fetch(`${API_BASE}/question/${domain}`);
    const data = await response.json();

    document.getElementById("questionBox").innerText = data.question_text;
    document.getElementById("answer").value = "";

    currentQuestionIndex++;
    updateProgress();
}



async function submitAnswer() {

    const answer = document.getElementById("answer").value;

    const response = await fetch(`${API_BASE}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            question_id: 1,  // replace with your stored question id logic if needed
            user_answer: answer
        })
    });

    const data = await response.json();

    sessionScores.push(data.score);

    document.getElementById("result").innerText =
        `Score: ${data.score} / 10`;
}
function updateProgress() {

    let percent = (currentQuestionIndex / totalQuestions) * 100;

    document.getElementById("progressBar").style.width = percent + "%";

    document.getElementById("progressText").innerText =
        `Question ${currentQuestionIndex} of ${totalQuestions}`;
}
function showSummary() {

    document.getElementById("sessionSummary").style.display = "block";

    const total = sessionScores.reduce((a, b) => a + b, 0);
    const average = total / sessionScores.length;

    document.getElementById("finalScore").innerText =
        `Your Average Score: ${average.toFixed(2)} / 10`;
}
function restartSession() {
    currentQuestionIndex = 0;
    sessionScores = [];
    document.getElementById("progressBar").style.width = "0%";
    document.getElementById("progressText").innerText = "";
    document.getElementById("sessionSummary").style.display = "none";
    document.getElementById("result").innerText = "";
    document.getElementById("questionBox").innerText = "Click Get Question to begin.";
}

async function loadAnalytics() {

    const response = await fetch(`${API_BASE}/analytics`);
    const data = await response.json();

    document.getElementById("total").innerText = data.total_attempts;
    document.getElementById("average").innerText = data.average_score;

    const domains = Object.keys(data.domain_performance);
    const scores = Object.values(data.domain_performance);

    const ctx = document.getElementById("domainChart");

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: domains,
            datasets: [{
                label: 'Average Score by Domain',
                data: scores,
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        }
    });
}

let mockQuestions = [];
let currentMockIndex = 0;
let mockScores = [];

async function startMock() {

    const response = await fetch(`${API_BASE}/mock/python`);
    mockQuestions = await response.json();

    currentMockIndex = 0;
    mockScores = [];

    document.getElementById("mockContent").style.display = "block";
    showMockQuestion();
}

function showMockQuestion() {
    if (currentMockIndex < mockQuestions.length) {
        document.getElementById("mockQuestion").innerText =
            mockQuestions[currentMockIndex].question_text;

        document.getElementById("mockAnswer").value = "";
    }
}

async function nextQuestion() {

    const answer = document.getElementById("mockAnswer").value;

    const response = await fetch(`${API_BASE}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            question_id: mockQuestions[currentMockIndex].id,
            user_answer: answer
        })
    });

    const data = await response.json();

    mockScores.push(data.score);
    currentMockIndex++;

    if (currentMockIndex < mockQuestions.length) {
        showMockQuestion();
    } else {
        finishMock();
    }
}

function finishMock() {

    const avg =
        mockScores.reduce((a, b) => a + b, 0) / mockScores.length;

    document.getElementById("mockContent").style.display = "none";
    document.getElementById("mockResult").innerText =
        "Interview Completed! Average Score: " + avg.toFixed(2) + " / 10";
}
