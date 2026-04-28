from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.notes import router as notes_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(notes_router)
