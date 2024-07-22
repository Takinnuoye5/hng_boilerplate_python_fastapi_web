import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes.newsletter_router import newsletter, CustomException, custom_exception_handler
from api.v1.routes.auth import auth
from api.v1.routes.user import user
from api.v1.routes.roles import role
from api.v1.routes.permission_router import router as permission_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(CustomException, custom_exception_handler)

app.include_router(newsletter, tags=["Newsletter"])
app.include_router(auth)
app.include_router(user)
app.include_router(role)
app.include_router(permission_router, tags=["Permissions"], prefix="/api/v1")

@app.get("/", tags=["Home"])
async def get_root():
    return {
        "message": "Welcome to API",
        "URL": "",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
