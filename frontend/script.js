const API_BASE = "https://abc123.ngrok-free.app";

let currentQuestionId = null;

async function getQuestion() {

    const domain = document.getElementById("domain").value;
    const difficulty = document.getElementById("difficulty").value;

    let url = `${API_BASE}/question/${domain}`;

    if (difficulty) {
        url += `?difficulty=${difficulty}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    currentQuestionId = data.id;

    document.getElementById("questionBox").innerText = data.question_text;
    document.getElementById("result").innerText = "";
    document.getElementById("answer").value = "";
}


async function submitAnswer() {

    const answer = document.getElementById("answer").value;

    if (!currentQuestionId) {
        alert("Please get a question first.");
        return;
    }

    if (!answer.trim()) {
        alert("Please enter your answer.");
        return;
    }

    const response = await fetch("${API_BASE}/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question_id: currentQuestionId,
            user_answer: answer
        })
    });

    const data = await response.json();

    document.getElementById("result").innerText =
        `Your Score: ${data.score} / 10`;
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
