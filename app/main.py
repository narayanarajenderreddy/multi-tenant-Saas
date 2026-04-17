
from fastapi import FastAPI
from app.api import auth
from app.api import tenant
from app.api import project
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

app = FastAPI()

from app.middleware.login_middleware import LoggingMiddleware

app.add_middleware(LoggingMiddleware)

from app.middleware.tenant_middleware import TenantMiddleware

app.add_middleware(TenantMiddleware)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


from app.core.exception import register_exception_handlers
register_exception_handlers(app)


@app.get("/")
def read_root():
    return {"message":"multi-tenant-system project started!"}

#auth api list.
app.include_router(auth.router)
app.include_router(tenant.router)
app.include_router(project.router)



