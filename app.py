from fastapi import FastAPI
import uvicorn
from config.db import db_ping
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="LMTSM Website")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from routes import auth
from routes import booking
from routes import roles

app.include_router(auth.router)
app.include_router(booking.router)
app.include_router(roles.router)


@app.on_event("startup")
async def startup():
    db_ping()


@app.get("/")
async def hello():
    return {"msg": "hello from the backend!"}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host="127.0.0.1", port=8100)
