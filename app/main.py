from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app=FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)
