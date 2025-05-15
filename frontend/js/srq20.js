// SRQ-20 Questionnaire Functions

// Load SRQ-20 questions
async function loadSRQ20Questions() {
  try {
    const questions = await apiRequest("/srq20/");
    if (!questions) return;

    const questionsList = document.getElementById("questionsList");
    if (!questionsList) return;

    // Clear the list
    questionsList.innerHTML = "";

    // Add each question
    questions.forEach((question) => {
      const questionItem = document.createElement("li");
      questionItem.className = "question-item";
      questionItem.dataset.questionId = question.id;

      questionItem.innerHTML = `
        <div class="question-text">${question.ordem}. ${question.texto}</div>
        <div class="question-options">
          <div>
            <input type="radio" name="question-${question.id}" id="question-${question.id}-yes" value="true" required>
            <label for="question-${question.id}-yes">Sim</label>
          </div>
          <div>
            <input type="radio" name="question-${question.id}" id="question-${question.id}-no" value="false" required>
            <label for="question-${question.id}-no">Não</label>
          </div>
        </div>
      `;

      questionsList.appendChild(questionItem);
    });

    // Initialize the form submission
    initSRQ20Form();
  } catch (error) {
    console.error("Error loading SRQ-20 questions:", error);
    showAlert("Erro ao carregar as perguntas do SRQ-20", "danger");
  }
}

// Submit SRQ-20 responses
async function submitSRQ20(responses) {
  try {
    const result = await apiRequest("/srq20/", "POST", {
      respostas: responses,
    });

    if (result) {
      // Store the result in localStorage for display
      localStorage.setItem("srq20Result", JSON.stringify(result));

      // Redirect to results page
      window.location.href = "resultado.html";
    }
  } catch (error) {
    console.error("Error submitting SRQ-20:", error);
    showAlert("Erro ao enviar as respostas", "danger");
  }
}

// Initialize the SRQ-20 form submission
function initSRQ20Form() {
  const form = document.getElementById("srq20Form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get all questions
    const questionItems = document.querySelectorAll(".question-item");
    const responses = [];
    let allAnswered = true;

    // Check if all questions are answered
    questionItems.forEach((item) => {
      const questionId = item.dataset.questionId;
      const selectedOption = form.querySelector(
        `input[name="question-${questionId}"]:checked`
      );

      if (!selectedOption) {
        allAnswered = false;
        return;
      }

      const response = {
        pergunta: parseInt(questionId),
        resposta: selectedOption.value === "true",
      };

      responses.push(response);
    });

    if (!allAnswered) {
      showAlert("Por favor, responda todas as perguntas", "warning");
      return;
    }

    await submitSRQ20(responses);
  });
}

// Display SRQ-20 results
function displaySRQ20Result() {
  const resultContainer = document.getElementById("resultContainer");
  if (!resultContainer) return;

  const resultData = localStorage.getItem("srq20Result");
  if (!resultData) {
    window.location.href = "srq20.html";
    return;
  }

  // Clear the loading indicator
  resultContainer.innerHTML = "";

  const result = JSON.parse(resultData);
  const { avaliacao, atividades_sugeridas } = result;

  // Display score and suffering level
  const resultCard = document.createElement("div");
  resultCard.className = "card result-card";

  let levelClass = "";
  switch (avaliacao.nivel_sofrimento) {
    case "Nenhum":
      levelClass = "level-none";
      break;
    case "Leve":
      levelClass = "level-mild";
      break;
    case "Moderado":
      levelClass = "level-moderate";
      break;
    case "Grave":
      levelClass = "level-severe";
      break;
  }

  resultCard.innerHTML = `
    <div class="result-score">${avaliacao.pontuacao_total}</div>
    <div class="result-level ${levelClass}">${avaliacao.nivel_sofrimento}</div>
    <p>Pontuação obtida na avaliação SRQ-20</p>
    <p>Data: ${new Date(avaliacao.data_avaliacao).toLocaleDateString()}</p>
  `;

  resultContainer.appendChild(resultCard);

  // Display suggested activities
  if (atividades_sugeridas && atividades_sugeridas.length > 0) {
    const activitiesCard = document.createElement("div");
    activitiesCard.className = "card";

    let activitiesHTML = `
      <h2 class="card-title">Atividades Sugeridas</h2>
      <div class="card-body">
        <ul class="activities-list">
    `;

    atividades_sugeridas.forEach((activity) => {
      activitiesHTML += `<li>${activity.descricao}</li>`;
    });

    activitiesHTML += `
        </ul>
      </div>
    `;

    activitiesCard.innerHTML = activitiesHTML;
    resultContainer.appendChild(activitiesCard);
  }
}

// Load user evaluation history
async function loadEvaluationHistory() {
  try {
    const evaluations = await apiRequest("/avaliacoes/");
    if (!evaluations) return;

    const historyContainer = document.getElementById("historyContainer");
    if (!historyContainer) return;

    // Clear the loading indicator
    historyContainer.innerHTML = "";

    if (evaluations.results && evaluations.results.length === 0) {
      historyContainer.innerHTML =
        '<div class="card"><p>Você ainda não realizou nenhuma avaliação SRQ-20.</p></div>';
      return;
    }

    const historyList = document.createElement("div");

    evaluations.results.forEach((evaluation) => {
      const historyItem = document.createElement("div");
      historyItem.className = "card history-item";
      historyItem.dataset.id = evaluation.id;

      let levelClass = "";
      switch (evaluation.nivel_sofrimento) {
        case "Nenhum":
          levelClass = "level-none";
          break;
        case "Leve":
          levelClass = "level-mild";
          break;
        case "Moderado":
          levelClass = "level-moderate";
          break;
        case "Grave":
          levelClass = "level-severe";
          break;
      }

      historyItem.innerHTML = `
        <div class="history-date">${new Date(
          evaluation.data_avaliacao
        ).toLocaleString()}</div>
        <div>
          <strong>Pontuação:</strong> ${evaluation.pontuacao_total}
          <span class="result-level ${levelClass}">${
        evaluation.nivel_sofrimento
      }</span>
        </div>
      `;

      historyList.appendChild(historyItem);
    });

    historyContainer.appendChild(historyList);
  } catch (error) {
    console.error("Error loading evaluation history:", error);
    showAlert("Erro ao carregar histórico de avaliações", "danger");
  }
}

// Initialize page-specific functionality
document.addEventListener("DOMContentLoaded", () => {
  // Redirect if not authenticated
  if (
    document.querySelector(".srq-page") ||
    document.querySelector(".result-page") ||
    document.querySelector(".history-page")
  ) {
    redirectIfNotAuthenticated();
  }

  // Load SRQ-20 questions if on questionnaire page
  if (document.querySelector(".srq-page")) {
    loadSRQ20Questions();
  }

  // Display results if on result page
  if (document.querySelector(".result-page")) {
    displaySRQ20Result();
  }

  // Load history if on history page
  if (document.querySelector(".history-page")) {
    loadEvaluationHistory();
  }
});
