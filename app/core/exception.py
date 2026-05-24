from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def business_exception_handler(request:Request, exc:HTTPException):
    """
    Ensures all 400 errors follow a clean, consistent format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content = {
            "error":"Business Rule Violation",
            "message": exc.detail,
            "path" : request.url.path
        }
    )