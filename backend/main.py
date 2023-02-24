from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.main import app as app_v1

app = FastAPI(

    title="DSC entrega 1",
    description="Entrega 1 Desarrollo de Soluciones Cloud",
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", app_v1)
