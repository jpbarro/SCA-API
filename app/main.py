from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import cats, missions, targets

app = FastAPI(title="Spy Cat Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cats.router)
app.include_router(missions.router)
app.include_router(targets.router)