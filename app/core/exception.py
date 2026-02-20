from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from app.schemas.common import ErrorResponse
from app.core.app_exception import AppException

import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    # 1 Custom Business Exceptions
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error(f"AppException: {exc.message}")

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=exc.message,
                error_code=exc.error_code,
                details=exc.details
            ).dict()
        )
        

    # 2 Handle HTTPException
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                 message=exc.detail,
                error_code="HTTP_ERROR"
            ).dict()
                
        )

    # 3 Handle Validation Errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                message="Validation error",
                error_code="VALIDATION_ERROR",
                details=exc.errors()
            ).dict()
        )
    
    
    #4.integrity error
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        logger.error(f"Integrity Error: {str(exc)}")

        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                message="Duplicate or invalid data",
                error_code="INTEGRITY_ERROR"
            ).dict()
        )
            

    # 5 Handle Database Errors
    @app.exception_handler(SQLAlchemyError)
    async def db_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Database error occurred",
                error_code="DATABASE_ERROR"
            ).dict()
        )

    # 6 Catch All Other Errors
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Internal server error",
                error_code="INTERNAL_SERVER_ERROR"
            ).dict()
        )
