from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import os
from starlette.responses import Response
#####
app = FastAPI()

# Get version information from environment variables
APP_VERSION = os.getenv("APP_VERSION", "dev")
GIT_SHA = os.getenv("GIT_SHA", "unknown")
BUILD_TIME = os.getenv("BUILD_TIME", "unknown")
APP_NAME='test-aoo'

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP Requests", ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds", "Request latency", ["endpoint"]
)

# Custom gauge for app version
APP_INFO = Gauge(
    "app_info", "Application info and version", ["version", "git_sha", "build_time"]
)

# Set the version and other metadata in the gauge
APP_INFO.labels(version=APP_VERSION, git_sha=GIT_SHA, build_time=BUILD_TIME, app_name=APP_NAME).set(1)

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    method = request.method

    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)

    return response

# Endpoints
@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

@app.get("/goodbye")
async def goodbye():
    return {"message": "Goodbye!"}

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
