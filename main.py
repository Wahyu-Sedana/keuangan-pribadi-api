from fastapi import FastAPI, Request
import time
from routes import auth, health, transaction
from database import Base, engine
from logger import log_info, log_error

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    log_info(f"{request.client.host} - {request.method} {request.url} - {response.status_code} - {process_time:.2f}s")

    return response

app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(health.router, prefix="", tags=["Health Check"])
app.include_router(transaction.router, prefix="", tags=["Transaction"])
