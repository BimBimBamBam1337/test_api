from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.api.routes import routes

# ------------------------------------------------------
# Главный FastAPI app
# ------------------------------------------------------
app = FastAPI(
    title="Functional API",
    version="1.0",
    description="Документация для функционального API с разграничением прав",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(routes[0], prefix="/api", tags=["Employee"])
app.include_router(routes[1], prefix="/api", tags=["Department"])


origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
