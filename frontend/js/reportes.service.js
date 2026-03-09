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

async function downloadFile(path, filename) {
  const token = getToken();
  const url = window.APP_CONFIG.API_BASE_URL + path;

  const res = await fetch(url, {
    method: "GET",
    headers: token ? { Authorization: "Bearer " + token } : {}
  });

  if (!res.ok) {
    let msg = `Error ${res.status}`;
    try {
      const data = await res.json();
      msg = data?.detail || data?.message || msg;
    } catch (_) {}
    throw new Error(msg);
  }

  const blob = await res.blob();
  const blobUrl = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = blobUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(blobUrl);
}

async function dashboardDownloadCsv() {
  return downloadFile(`${epReportes()}/dashboard/csv`, "dashboard_report.csv");
}

async function dashboardDownloadExcel() {
  return downloadFile(`${epReportes()}/dashboard/excel`, "dashboard_report.xlsx");
}