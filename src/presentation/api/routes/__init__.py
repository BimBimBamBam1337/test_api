from .user_router import router as user_router
from .role_router import router as role_router
from .session_router import router as session_router
from .refresh_token_router import (
    router as refresh_token_router,
)
from .buisness_elements_router import (
    router as buisness_element_router,
)
from .access_role_rules_router import (
    router as access_role_rules_router,
)

routers = [
    user_router,
    role_router,
    session_router,
    refresh_token_router,
    buisness_element_router,
    access_role_rules_router,
]
