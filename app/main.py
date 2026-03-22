from fastapi import FastAPI

from app.database import Base, engine
from app.routers import credits, performance, plans

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Management API")

app.include_router(credits.router)
app.include_router(plans.router)
app.include_router(performance.router)
