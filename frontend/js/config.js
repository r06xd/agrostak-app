// Cambia SOLO estos valores según tu backend real:
window.APP_CONFIG = {
  API_BASE_URL: "https://agrostak-backend.onrender.com",
  //API_BASE_URL: "http://127.0.0.1:8000",
  ENDPOINTS: {
    LOGIN: "/identity/login",
    MENU: "/identity/menu",
    RECURSOS: "/recursos",
    ROLES: "/identity/roles",
    USUARIOS: "/identity/usuarios",
    TAREAS: "/tareas",
    REPORTES: "/reports",
    REPORTES_GENERAR: "/reportes/generar",
    DASHBOARD_SUMMARY: "/reports/dashboard"
  },
  STORAGE: {
    TOKEN_KEY: "omar_access_token",
    MENU_KEY: "omar_menu"
  }
};

