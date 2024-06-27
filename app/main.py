from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import logging

logging.basicConfig(level=logging.INFO)

class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        logging.info(f"Handling request: {request.method} {request.url}")
        origin = request.headers.get("Origin")
        
        if request.method == "OPTIONS":
            response = Response()
            response.status_code = 204
            response.headers["Access-Control-Allow-Origin"] = origin if origin else "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            logging.info(f"Preflight request from {origin}")
            return response
        
        response = await call_next(request)
        
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
        
        logging.info(f"Completed request from {origin}")
        return response

app = FastAPI()

# Ensure DynamicCORSMiddleware is added before other middlewares
app.add_middleware(DynamicCORSMiddleware)

# Include your routers
from app.routers import ocr, user, auth
app.include_router(ocr.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to MedscanRx"}
