// Cambia SOLO estos valores según tu backend real:
window.APP_CONFIG = {
  API_BASE_URL: "http://127.0.0.1:8000",
  ENDPOINTS: {
    LOGIN: "/identity/login",
    RECURSOS: "/recursos" // <-- luego lo ajustamos cuando me pases el endpoint real
  },
  STORAGE: {
    TOKEN_KEY: "omar_access_token"
  }
};

