from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from tasks.routes import router as task_routers
from users.routes import router as users_routers


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

from auth.jwt_auth import get_authenticated_user


@app.get("/private")
async def private_route(user=Depends(get_authenticated_user)):
    print(user)
    return {"massage": "This is a private route."}
