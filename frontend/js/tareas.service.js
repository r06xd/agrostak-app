function epTareas() {
  return window.APP_CONFIG.ENDPOINTS.TAREAS;
}

async function tareasList() {
  return apiRequest(epTareas(), { method: "GET" });
}

async function tareasGetById(id) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id)}`, { method: "GET" });
}

async function tareasCreate(payload) {
  return apiRequest(epTareas(), { method: "POST", body: payload });
}

async function tareasUpdate(id, payload) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id)}`, { method: "PUT", body: payload });
}

async function tareasDelete(id) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id)}`, { method: "DELETE" });
}
