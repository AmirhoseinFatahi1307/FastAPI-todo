from fastapi import FastAPI, Depends, Response, Request
from contextlib import asynccontextmanager
from tasks.routes import router as task_routers
from users.routes import router as users_routers
from auth.jwt_auth import get_authenticated_user
from fastapi.middleware.cors import CORSMiddleware
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


metadata_tags = [
    {"name": "Tasks", "description": "Operation related to task management"}
]


app = FastAPI(
    title="Todo Application",
    contact={
        "name": "AmirhoseinFatahi1307",
        "email": "fatahiamirhosein8@gmail.com",
        "url": "https://www.linkedin.com/in/amirhosein-fatahi-64b797413/",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=metadata_tags,
)

app.include_router(task_routers)
app.include_router(users_routers)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = ["http://127.0.0.1:5500"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
