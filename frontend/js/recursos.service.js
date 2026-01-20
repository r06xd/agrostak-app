function epRecursos() {
  return window.APP_CONFIG.ENDPOINTS.RECURSOS;
}

async function recursosList() {
  return apiRequest(epRecursos(), { method: "GET" });
}

async function recursosGetById(id) {
  return apiRequest(`${epRecursos()}/${encodeURIComponent(id)}`, { method: "GET" });
}

async function recursosCreate(payload) {
  return apiRequest(epRecursos(), { method: "POST", body: payload });
}

async function recursosUpdate(id, payload) {
  return apiRequest(`${epRecursos()}/${encodeURIComponent(id)}`, { method: "PUT", body: payload });
}

async function recursosDelete(id) {
  return apiRequest(`${epRecursos()}/${encodeURIComponent(id)}`, { method: "DELETE" });
}
