function epTareas() {
  return window.APP_CONFIG.ENDPOINTS.TAREAS;
}

async function tareasList() {
  return apiRequest(epTareas(), { method: "GET" });
}

async function tareasListByUsuarios() {
  return apiRequest(`${epTareas()}/my`, { method: "GET" });
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

/**
 * POST /tasks/{id_tarea}/assignUser/{id_usuario}
 * Body: AsignacionCreate
 */
async function tareasAsignar(id_tarea, id_usuario) {
  return apiRequest(
    `${epTareas()}/${encodeURIComponent(id_tarea)}/assignUser/${encodeURIComponent(id_usuario)}`,
    {
      method: "POST",
      body: {id_usuario: id_usuario},   // AsignacionCreate (si tiene campos extra)
      auth: true
    }
  );
}
