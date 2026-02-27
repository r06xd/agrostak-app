function epUsuarios(){ return window.APP_CONFIG.ENDPOINTS.USUARIOS; }

async function usuariosList(){ return apiRequest(epUsuarios(), { method:"GET" }); }
async function usuariosGetById(id){ return apiRequest(`${epUsuarios()}/porId/${encodeURIComponent(id)}`, { method:"GET" }); }
async function usuariosCreate(payload){ return apiRequest(epUsuarios(), { method:"POST", body: payload }); }
async function usuariosUpdate(id, payload){ return apiRequest(`${epUsuarios()}/${encodeURIComponent(id)}`, { method:"PUT", body: payload }); }
async function usuariosDelete(id){ return apiRequest(`${epUsuarios()}/${encodeURIComponent(id)}`, { method:"DELETE" }); }
