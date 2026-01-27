async function fetchMenuFromApi() {
  const ep = window.APP_CONFIG.ENDPOINTS.MENU;
  console.log(ep);
  return apiRequest(ep, { method: "GET", auth: true });
}

function saveMenu(menuArray) {
  localStorage.setItem(window.APP_CONFIG.STORAGE.MENU_KEY, JSON.stringify(menuArray || []));
}

function loadMenu() {
  try {
    const raw = localStorage.getItem(window.APP_CONFIG.STORAGE.MENU_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function clearMenu() {
  localStorage.removeItem(window.APP_CONFIG.STORAGE.MENU_KEY);
}
