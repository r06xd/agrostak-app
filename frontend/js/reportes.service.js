function epReportes(){ return window.APP_CONFIG.ENDPOINTS.REPORTES; }
function epGenerar(){ return window.APP_CONFIG.ENDPOINTS.REPORTES_GENERAR; }
function epDashboardSummary(){return window.APP_CONFIG.ENDPOINTS.DASHBOARD_SUMMARY;}

async function reportesList(){
  return apiRequest(epReportes(), { method: "GET", auth: true });
}

async function reportesGetById(id){
  return apiRequest(`${epReportes()}/${encodeURIComponent(id)}`, { method: "GET", auth: true });
}

async function reportesGetDashboard(){
  return apiRequest(`${epReportes()}/dashboard`, { method: "GET", auth: true });
}

/**
 * Generar reporte (ejemplo):
 * payload: { tipo:"tareas", formato:"pdf", desde:"2026-02-01", hasta:"2026-02-10" }
 */
async function reportesGenerar(payload){
  return apiRequest(epGenerar(), { method: "POST", body: payload, auth: true });
}

async function dashboardSummaryGet(){
  return apiRequest(epDashboardSummary(), { method: "GET", auth: true });
}