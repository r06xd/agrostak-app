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
  return data;
}

function requireAuthOrRedirect() {
  const token = getToken();
  if (!token) window.location.href = "./login.html";
}

function logout() {
  clearToken();
  window.location.href = "./login.html";
}
