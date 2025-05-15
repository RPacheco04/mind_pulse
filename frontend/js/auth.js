// Authentication Functions

// Login function
async function login(username, password) {
  try {
    showLoading();
    const response = await fetch(`${API_URL}/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMessage =
        data.detail || "Falha no login. Verifique suas credenciais.";
      throw new Error(errorMessage);
    }

    // Store the token in local storage
    localStorage.setItem("authToken", data.access);
    localStorage.setItem("refreshToken", data.refresh);

    // Fetch user information
    await fetchUserInfo();

    // Redirect to home page
    window.location.href = "index.html";
  } catch (error) {
    console.error("Login error:", error);
    showAlert(error.message, "danger");
  } finally {
    hideLoading();
  }
}

// Register function
async function register(userData) {
  try {
    showLoading();
    const response = await fetch(`${API_URL}/registro/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();

    if (!response.ok) {
      let errorMessage = "Falha no cadastro. Verifique seus dados.";

      // Format validation errors
      if (data.username) {
        errorMessage = `Nome de usuário: ${data.username.join(" ")}`;
      } else if (data.email) {
        errorMessage = `Email: ${data.email.join(" ")}`;
      } else if (data.password) {
        errorMessage = `Senha: ${data.password.join(" ")}`;
      }

      throw new Error(errorMessage);
    }

    showAlert(
      "Cadastro realizado com sucesso! Faça login para continuar.",
      "success"
    );

    // Redirect to login page after a short delay
    setTimeout(() => {
      window.location.href = "login.html";
    }, 1500);
  } catch (error) {
    console.error("Register error:", error);
    showAlert(error.message, "danger");
  } finally {
    hideLoading();
  }
}

// Fetch user information
async function fetchUserInfo() {
  try {
    const userData = await apiRequest("/usuarios/me/");
    if (userData) {
      localStorage.setItem("userInfo", JSON.stringify(userData));
    }
    return userData;
  } catch (error) {
    console.error("Error fetching user info:", error);
    return null;
  }
}

// Get current user information
function getCurrentUser() {
  const userInfo = localStorage.getItem("userInfo");
  return userInfo ? JSON.parse(userInfo) : null;
}

// Form validation functions
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validatePassword(password) {
  // At least 8 characters, one lowercase, one uppercase, one number, one special
  return password.length >= 8;
}

function validateRequired(value) {
  return value.trim() !== "";
}

function validateForm(form) {
  let isValid = true;
  const errors = {};

  // Get all required inputs
  const requiredInputs = form.querySelectorAll("[required]");

  requiredInputs.forEach((input) => {
    // Reset previous errors
    const errorElement = document.getElementById(`${input.id}-error`);
    if (errorElement) {
      errorElement.textContent = "";
    }

    if (!validateRequired(input.value)) {
      isValid = false;
      errors[input.id] = "Este campo é obrigatório";
    } else if (input.type === "email" && !validateEmail(input.value)) {
      isValid = false;
      errors[input.id] = "Email inválido";
    } else if (input.id === "password" && !validatePassword(input.value)) {
      isValid = false;
      errors[input.id] = "A senha deve ter pelo menos 8 caracteres";
    } else if (
      input.id === "password2" &&
      input.value !== form.querySelector("#password").value
    ) {
      isValid = false;
      errors[input.id] = "As senhas não conferem";
    }
  });

  // Display errors
  Object.keys(errors).forEach((inputId) => {
    const errorElement = document.getElementById(`${inputId}-error`);
    if (errorElement) {
      errorElement.textContent = errors[inputId];
    }
  });

  return isValid;
}

// Initialize login form
function initLoginForm() {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (validateForm(loginForm)) {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        await login(username, password);
      }
    });
  }
}

// Initialize register form
function initRegisterForm() {
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (validateForm(registerForm)) {
        const userData = {
          username: document.getElementById("username").value,
          email: document.getElementById("email").value,
          password: document.getElementById("password").value,
          password2: document.getElementById("password2").value,
          first_name: document.getElementById("firstName").value || "",
          last_name: document.getElementById("lastName").value || "",
          genero: document.getElementById("gender").value || null,
          data_nascimento: document.getElementById("birthDate").value || null,
        };

        await register(userData);
      }
    });
  }
}

// Initialize auth-related forms when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  initLoginForm();
  initRegisterForm();

  // Check if user is already authenticated
  if (document.querySelector(".auth-page")) {
    redirectIfAuthenticated();
  }
});
