let domainChartInstance = null;
let difficultyChartInstance = null;

async function loadAnalytics(category = null) {

    let url = `${API_BASE}/analytics`;

    if (category) {
        url += `?category=${category}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    document.getElementById("total").innerText = data.total_attempts;
    document.getElementById("average").innerText =
        data.average_score.toFixed(2);

    // DOMAIN BAR CHART
    const domains = Object.keys(data.domain_performance);
    const scores = Object.values(data.domain_performance);

    const ctx1 = document.getElementById("domainChart");

    if (domainChartInstance) {
        domainChartInstance.destroy();
    }

    domainChartInstance = new Chart(ctx1, {
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

    // DIFFICULTY PIE CHART
    const difficultyCounts = data.difficulty_breakdown;

    const ctx2 = document.getElementById("difficultyChart");

    if (difficultyChartInstance) {
        difficultyChartInstance.destroy();
    }

    difficultyChartInstance = new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: Object.keys(difficultyCounts),
            datasets: [{
                data: Object.values(difficultyCounts),
                backgroundColor: [
                    '#28a745',
                    '#ffc107',
                    '#dc3545'
                ]
            }]
        }
    });
    window.onload = function () {
        loadAnalytics("coding");
    };
}
