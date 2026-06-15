from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_scans import router as scans_router
from app.api.routes_stats import router as stats_router
from app.api.routes_products import router as products_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.scan import Scan  # noqa: F401


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans_router)
app.include_router(stats_router)
app.include_router(products_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}