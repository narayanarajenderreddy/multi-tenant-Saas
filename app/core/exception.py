from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app):

    # 1️⃣ Handle HTTPException
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "error_code": "HTTP_ERROR"
            }
        )

    # 2️⃣ Handle Validation Errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "errors": exc.errors(),
                "error_code": "VALIDATION_ERROR"
            }
        )
    
    
    
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        logger.error(f"Integrity Error: {str(exc)}")

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Duplicate or invalid data",
                "error_code": "INTEGRITY_ERROR"
            }
        )
            

    # 3️⃣ Handle Database Errors
    @app.exception_handler(SQLAlchemyError)
    async def db_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Database error occurred",
                "error_code": "DATABASE_ERROR"
            }
        )

    # 4️⃣ Catch All Other Errors
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Something went wrong",
                "error_code": "INTERNAL_SERVER_ERROR"
            }
        )
