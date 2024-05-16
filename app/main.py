from fastapi import FastAPI

from .routers import leads, login

app = FastAPI(title="FastAPI to Support Leads Operations")

app.include_router(login.router, tags=["login"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])
