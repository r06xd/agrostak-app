async function loginRequest(correo, password) {
  const ep = window.APP_CONFIG.ENDPOINTS.LOGIN;

  const data = await apiRequest(ep, {
    method: "POST",
    body: { correo, password },
    auth: false
  });

  console.log(data);

  const token = data?.access_token;
  if (!token) throw new Error("No se recibió access_token del servidor.");

  setToken(token);

  // Cargar menú por rol y guardarlo
  try {
    
    const menu = await fetchMenuFromApi();
    const menuArray = Array.isArray(menu) ? menu : (menu?.data || []);
    saveMenu(menuArray);
  } catch (e) {
    console.log("Entra al catch");
    // si falla, igual deja loguear, pero sin menú
    saveMenu([]);
  }

  return data;
}

function requireAuthOrRedirect() {
  const token = getToken();
  if (!token) window.location.href = "./index.html";
}

function logout() {
  clearToken();
  window.location.href = "../../index.html";
}
