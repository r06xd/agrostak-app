function getToken() {
  return localStorage.getItem(window.APP_CONFIG.STORAGE.TOKEN_KEY) || "";
}

function setToken(token) {
  localStorage.setItem(window.APP_CONFIG.STORAGE.TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(window.APP_CONFIG.STORAGE.TOKEN_KEY);
}

async function apiRequest(path, { method = "GET", body = null, auth = true } = {}) {
  const url = window.APP_CONFIG.API_BASE_URL + path;

  const headers = { "Content-Type": "application/json" };

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = "Bearer " + token;
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (_) {}

  if (!res.ok) {
    const msg = (data && (data.message || data.detail)) || `Error ${res.status}`;
    throw new Error(msg);
  }

  return data;
}
