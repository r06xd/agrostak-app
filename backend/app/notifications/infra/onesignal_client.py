import os
import requests

ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_REST_API_KEY = os.getenv("ONESIGNAL_REST_API_KEY")

def send_task_assigned_push(id_usuario: int, titulo_tarea: str, id_tarea: int):
    url = "https://onesignal.com/api/v1/notifications"
    print("entra a enviar notificacion=========>")
    print(ONESIGNAL_APP_ID)
    print(ONESIGNAL_REST_API_KEY)
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_external_user_ids": [str(id_usuario)],  # <- SOLO ese usuario
        "contents": {"en": f"Te asignaron una tarea: {titulo_tarea}", "es": f"Te asignaron una tarea: {titulo_tarea}"},
        "headings": {"en": "Nueva tarea asignada", "es": "Nueva tarea asignada"},
        "data": {"id_tarea": id_tarea, "tipo": "tarea_asignada"},
        # opcional: URL a la que abre al hacer click
        "url": f"https://TU_FRONTEND_NETLIFY_URL/#/tareas/{id_tarea}"
    }
    print("pudo generar el mrensae")
    headers = {
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers, timeout=15)
    r.raise_for_status()
    print("pudo enviar notificacion")
    print("STATUS",r.status_code)
    print("RESPONSE",r.text)
    return r.json()
