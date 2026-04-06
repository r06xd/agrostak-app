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

function epRecursos(){
  return window.APP_CONFIG.ENDPOINTS.RECURSOS;
}

function epAsignarRecurso(idTarea,idRecurso){
  return "/tasks/assignResource/"+idTarea+"/"+idRecurso;
}

async function getRecursos(){

  return apiRequest(epRecursos(), {
    method:"GET",
    auth:true
  });

}

async function tareasAsignarRecurso(id_tarea, id_recurso, cantidad) {
  return apiRequest(
    `/recursos/assignResource/${encodeURIComponent(id_tarea)}/${encodeURIComponent(id_recurso)}/${encodeURIComponent(cantidad)}`,
    {
      method: "POST",
      auth: true
    }
  );
}

async function tareasListRecursos(id_tarea) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id_tarea)}/resources`, {
    method: "GET",
    auth: true
  });
}

async function tareasEliminarRecurso(id_tarea, id_tarea_recurso) {
  return apiRequest(
    `${epTareas()}/${encodeURIComponent(id_tarea)}/resources/${encodeURIComponent(id_tarea_recurso)}`,
    {
      method: "DELETE",
      auth: true
    }
  );
}

async function actualizarEstadoTarea(id_tarea, estado){
  return apiRequest(
    `${epTareas()}/${encodeURIComponent(id_tarea)}/status`,
    {
      method: "POST",
      body: {estado: estado},
      auth: true
    }
  );
}

async function tareasListComments(id_tarea) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id_tarea)}/comments`, {
    method: "GET",
    auth: true
  });
}

async function tareasAddComment(id_tarea, payload) {
  return apiRequest(`${epTareas()}/${encodeURIComponent(id_tarea)}/comments`, {
    method: "POST",
    body: payload,
    auth: true
  });
}
