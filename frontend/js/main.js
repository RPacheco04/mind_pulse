// Configuration
const API_URL = "http://localhost:8000/api";

// Helper Functions
function showLoading() {
  const loadingEl = document.createElement("div");
  loadingEl.className = "loading";
  loadingEl.innerHTML = '<div class="loading-spinner"></div>';
  document.body.appendChild(loadingEl);
}

function hideLoading() {
  const loadingEl = document.querySelector(".loading");
  if (loadingEl) {
    loadingEl.remove();
  }
}

function showAlert(message, type = "info") {
  const alertEl = document.createElement("div");
  alertEl.className = `alert alert-${type}`;
  alertEl.textContent = message;

  const container = document.querySelector(".container");
  container.insertBefore(alertEl, container.firstChild);

  // Auto-hide after 5 seconds
  setTimeout(() => {
    alertEl.remove();
  }, 5000);
}

function getAuthToken() {
  return localStorage.getItem("authToken");
}

function isAuthenticated() {
  return !!getAuthToken();
}

function redirectIfNotAuthenticated() {
  if (!isAuthenticated()) {
    window.location.href = "login.html";
  }
}

function redirectIfAuthenticated() {
  if (isAuthenticated()) {
    window.location.href = "index.html";
  }
}

// API Functions
async function apiRequest(endpoint, method = "GET", data = null) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (isAuthenticated()) {
    headers["Authorization"] = `Bearer ${getAuthToken()}`;
  }

  const config = {
    method,
    headers,
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  try {
    showLoading();
    const response = await fetch(`${API_URL}${endpoint}`, config);

    if (response.status === 401) {
      // Unauthorized - token expired
      localStorage.removeItem("authToken");
      window.location.href = "login.html";
      return null;
    }

    const responseData = await response.json();

    if (!response.ok) {
      throw new Error(responseData.error || "Algo deu errado");
    }

    return responseData;
  } catch (error) {
    console.error("API Error:", error);
    showAlert(error.message, "danger");
    return null;
  } finally {
    hideLoading();
  }
}

// Event Listeners for Navigation
document.addEventListener("DOMContentLoaded", () => {
  // Update navigation based on authentication
  const navEl = document.querySelector("nav ul");

  if (navEl) {
    if (isAuthenticated()) {
      navEl.innerHTML = `
        <li><a href="index.html">Início</a></li>
        <li><a href="srq20.html">Questionário SRQ-20</a></li>
        <li><a href="historico.html">Histórico</a></li>
        <li><a href="#" id="logoutBtn">Sair</a></li>
      `;

      // Add logout functionality
      document.getElementById("logoutBtn")?.addEventListener("click", (e) => {
        e.preventDefault();
        localStorage.removeItem("authToken");
        window.location.href = "login.html";
      });
    } else {
      navEl.innerHTML = `
        <li><a href="index.html">Início</a></li>
        <li><a href="login.html">Entrar</a></li>
        <li><a href="cadastro.html">Cadastrar</a></li>
      `;
    }
  }
});
