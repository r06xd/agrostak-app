function epRoles(){ return window.APP_CONFIG.ENDPOINTS.ROLES; }

async function rolesList(){ return apiRequest(epRoles(), { method:"GET" }); }
async function rolesGetById(id){ return apiRequest(`${epRoles()}/${encodeURIComponent(id)}`, { method:"GET" }); }
async function rolesCreate(payload){ return apiRequest(epRoles(), { method:"POST", body: payload }); }
async function rolesUpdate(id, payload){ return apiRequest(`${epRoles()}/${encodeURIComponent(id)}`, { method:"PUT", body: payload }); }
async function rolesDelete(id){ return apiRequest(`${epRoles()}/${encodeURIComponent(id)}`, { method:"DELETE" }); }
