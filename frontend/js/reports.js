// Reports and Metrics Functions

// Load metrics data
async function loadMetrics() {
  try {
    // Only admin users should be able to access this
    const currentUser = getCurrentUser();
    if (!currentUser || !currentUser.is_staff) {
      showAlert("Você não tem permissão para acessar esta página.", "danger");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 2000);
      return;
    }

    const metricsData = await apiRequest("/avaliacoes/estatisticas/");
    if (!metricsData) return;

    displayMetrics(metricsData);
  } catch (error) {
    console.error("Error loading metrics:", error);
    showAlert("Erro ao carregar métricas", "danger");
  }
}

// Display metrics
function displayMetrics(data) {
  const metricsContainer = document.getElementById("metricsContainer");
  if (!metricsContainer) return;

  // General statistics
  const generalStatsCard = document.createElement("div");
  generalStatsCard.className = "card";
  generalStatsCard.innerHTML = `
    <h2 class="card-title">Estatísticas Gerais</h2>
    <div class="card-body">
      <p><strong>Total de Avaliações:</strong> ${data.total_avaliacoes}</p>
      <p><strong>Pontuação Média:</strong> ${
        data.media_pontuacao ? data.media_pontuacao.toFixed(2) : "N/A"
      }</p>
    </div>
  `;
  metricsContainer.appendChild(generalStatsCard);

  // Distribution by suffering level
  const levelDistributionCard = document.createElement("div");
  levelDistributionCard.className = "card";
  levelDistributionCard.innerHTML = `
    <h2 class="card-title">Distribuição por Nível de Sofrimento</h2>
    <div class="card-body">
      <div class="chart-container">
        <canvas id="levelDistributionChart"></canvas>
      </div>
    </div>
  `;
  metricsContainer.appendChild(levelDistributionCard);

  // Distribution by gender
  if (data.por_genero && data.por_genero.length > 0) {
    const genderCard = document.createElement("div");
    genderCard.className = "card";
    genderCard.innerHTML = `
      <h2 class="card-title">Distribuição por Gênero</h2>
      <div class="card-body">
        <div class="chart-container">
          <canvas id="genderChart"></canvas>
        </div>
      </div>
    `;
    metricsContainer.appendChild(genderCard);
  }

  // Data export section
  const exportCard = document.createElement("div");
  exportCard.className = "card";
  exportCard.innerHTML = `
    <h2 class="card-title">Exportar Dados</h2>
    <div class="card-body">
      <p>Faça o download dos dados em diferentes formatos:</p>
      <div class="mt-3">
        <a href="${API_URL}/avaliacoes/export/?formato=json" class="btn btn-primary" target="_blank">Download JSON</a>
        <a href="${API_URL}/avaliacoes/export/?formato=csv" class="btn btn-secondary" target="_blank" style="margin-left: 10px;">Download CSV</a>
      </div>
    </div>
  `;
  metricsContainer.appendChild(exportCard);

  // Initialize charts after appending to DOM
  initCharts(data);
}

// Initialize charts
function initCharts(data) {
  // Load Chart.js library dynamically
  if (!window.Chart) {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
    script.onload = () => createCharts(data);
    document.head.appendChild(script);
  } else {
    createCharts(data);
  }
}

// Create charts
function createCharts(data) {
  // Level distribution chart
  if (data.distribuicao_niveis && data.distribuicao_niveis.length > 0) {
    const ctx = document.getElementById("levelDistributionChart");
    if (ctx) {
      const labels = data.distribuicao_niveis.map(
        (item) => item.nivel_sofrimento
      );
      const values = data.distribuicao_niveis.map((item) => item.total);

      new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              data: values,
              backgroundColor: [
                "#d6eaf8", // None
                "#d4efdf", // Mild
                "#fdebd0", // Moderate
                "#f9ebea", // Severe
              ],
              borderColor: [
                "#2874a6", // None
                "#239b56", // Mild
                "#b9770e", // Moderate
                "#b03a2e", // Severe
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Distribuição por Nível de Sofrimento",
            },
          },
        },
      });
    }
  }

  // Gender distribution chart
  if (data.por_genero && data.por_genero.length > 0) {
    const ctx = document.getElementById("genderChart");
    if (ctx) {
      const labels = data.por_genero.map(
        (item) => item.usuario__genero || "Não informado"
      );
      const values = data.por_genero.map((item) => item.media);

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Pontuação média por gênero",
              data: values,
              backgroundColor: "#3498db",
              borderColor: "#2980b9",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 20,
              title: {
                display: true,
                text: "Pontuação média",
              },
            },
            x: {
              title: {
                display: true,
                text: "Gênero",
              },
            },
          },
          plugins: {
            title: {
              display: true,
              text: "Pontuação média por gênero",
            },
          },
        },
      });
    }
  }
}

// Initialize the reports page
document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector(".metrics-page")) {
    redirectIfNotAuthenticated();
    loadMetrics();
  }
});
