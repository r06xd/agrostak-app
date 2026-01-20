from fastapi import FastAPI
from app.shared.db import engine
from app.shared.base_model import Base
from app.resources.infra.models import RecursoORM  # importa modelos para que SQLAlchemy los conozca
from app.resources.api.router import router as recursos_router
from app.identity.api.router import router as identity_router
from app.identity.infra.models import RolORM, UsuarioORM, AccesoUsuarioORM
from app.tasks.api.router import router as tasks_router
from app.tasks.infra.models import TareaORM, AsignacionTareaORM, HistorialEstadoTareaORM, ComentarioTareaORM
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API Flor de Canela - Recursos")

#para pruebas locales
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],   # Authorization, Content-Type, etc.
)

# Crea las tablas si no existen
#Base.metadata.create_all(bind=engine)

# Rutas del módulo de recursos
app.include_router(recursos_router)
app.include_router(identity_router)
app.include_router(tasks_router)
