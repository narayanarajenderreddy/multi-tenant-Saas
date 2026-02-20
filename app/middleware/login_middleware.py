import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(f"[{request_id}] Started {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"[{request_id}] Completed {response.status_code} in {process_time}ms"
        )

        response.headers["X-Request-ID"] = request_id

        return response
