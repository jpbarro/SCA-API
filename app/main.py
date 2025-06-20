from fastapi import FastAPI
from .routers import cats, missions, targets

app = FastAPI(title="Spy Cat Agency API")

app.include_router(cats.router)
app.include_router(missions.router)
app.include_router(targets.router)