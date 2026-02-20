from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.dependencies.auth import get_current_user
from app.db.session import SessionLocal
from jose import jwt
from app.core.config import settings


class TenantMiddleware(BaseHTTPMiddleware):

    # async def dispatch(self, request: Request, call_next):
    #     body = await request.body()
    #     print("Raw Body:", body.decode())

    #     request.state.tenant_id = None

    #     # Only apply to protected routes
    #     if "authorization" in request.headers:

    #         db = SessionLocal()
    #         try:
    #             user = await get_current_user(request=request, db=db)
    #             request.state.tenant_id = user.tenant_id
    #         except:
    #             pass
    #         finally:
    #             db.close()

    #     response = await call_next(request)
    #     return response
    
    async def dispatch(self, request: Request, call_next):

        request.state.tenant_id = None

        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM]
                )

                request.state.tenant_id = payload.get("tenant_id")

            except Exception as e:
                print("Token decode failed:", str(e))

        response = await call_next(request)
        return response
    
    