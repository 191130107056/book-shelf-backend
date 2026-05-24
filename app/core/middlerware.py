# Simple In-Memory Rate Limiter 
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


user_requests = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Initialize or clean up old requests
        if client_ip not in user_requests:
            user_requests[client_ip] = []

        # Only keep requests from the last 60 seconds
        user_requests[client_ip] = [t for t in user_requests[client_ip] if current_time - t < 60]

        if len(user_requests[client_ip]) >= 10: # Limit: 10 requests per minute
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please wait a minute."}
            )
        
        # Record this request
        user_requests[client_ip].append(current_time)

        # Proceed to the actual API route
        response = await call_next(request)
        return response