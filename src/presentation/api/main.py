from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.api.routes import routers

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

app.include_router(routers[0], prefix="/api/v1", tags=["Users"])
app.include_router(routers[1], prefix="/api/v1", tags=["Roles"])
app.include_router(routers[2], prefix="/api/v1", tags=["Sessions"])
app.include_router(routers[3], prefix="/api/v1", tags=["RefreshTokens"])
app.include_router(
    routers[4],
    prefix="/api/v1",
    tags=["BuisnessElements"],
)
app.include_router(
    routers[5],
    prefix="/api/v1",
    tags=["AccessRoleRules"],
)
app.include_router(
    routers[6],
    prefix="/api/v1",
    tags=["Auth"],
)

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

# ------------------------------------------------------
# Взаимодействие с пользователем
# ------------------------------------------------------
# 1. Регистрация, Login, Logout, Update profile, Soft Delete
# 2. После login используется идентификация пользователя через токен
# 3. Мягкое удаление (is_active=False)
# 4. Ограничение доступа по ролям и правилам в handler/сервисах

# Все проверки авторизации и доступа реализуются в зависимости get_user_from_verify_token
# и в хендлерах (например, UsersHandler, AccessRoleRulesHandler) через NotPermissionError
