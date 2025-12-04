from fastapi import FastAPI

from config import settings
from presentation.api.routes.user_router import router as user_router
from presentation.api.routes.role_router import router as role_router
from presentation.api.routes.session_router import router as session_router
from presentation.api.routes.refresh_token_router import (
    router as refresh_token_router,
)
from presentation.api.routes.buisness_elements_router import (
    router as buisness_element_router,
)
from presentation.api.routes.access_role_rules_router import (
    router as access_role_rules_router,
)

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


app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(role_router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(session_router, prefix="/api/v1/sessions", tags=["Sessions"])
app.include_router(
    refresh_token_router, prefix="/api/v1/refresh-tokens", tags=["RefreshTokens"]
)
app.include_router(
    buisness_element_router,
    prefix="/api/v1/buisness-elements",
    tags=["BuisnessElements"],
)
app.include_router(
    access_role_rules_router,
    prefix="/api/v1/access-role-rules",
    tags=["AccessRoleRules"],
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
