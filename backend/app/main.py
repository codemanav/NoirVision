"""
NoirVision backend: FastAPI app with TwelveLabs video analysis pipeline.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import users, videos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup. S3 and TwelveLabs are only required when calling /api/videos/* (checked there)."""
    s = get_settings()
    cognito_ok = bool(s.cognito_user_pool_id and s.cognito_user_pool_id.strip())
    logger.info("NoirVision backend starting; Cognito configured=%s", cognito_ok)
    if not cognito_ok:
        logger.warning("Set COGNITO_USER_POOL_ID (and COGNITO_REGION) in backend/.env for /api/users/me/*")
    yield
    pass


# TODO(production): Add auth dependency (e.g. JWT or API key) and use on protected routes.
# Demo mode: no auth; all routes are open.

app = FastAPI(
    title="NoirVision Backend",
    description="TwelveLabs video analysis pipeline; Evidence Pack API for claim scoring and RAG.",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videos.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}


# Consistent error JSON: FastAPI already returns {"detail": ...} for HTTPException
