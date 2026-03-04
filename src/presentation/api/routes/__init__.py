from .employee_router import router as employee_router
from .department_router import router as department_router

routes = [employee_router, department_router]
