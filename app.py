import uvicorn
from fastapi import FastAPI

from db.session import init_db
from routes.answer import a_router
from routes.question import q_router

app = FastAPI()

@app.on_event("startup")
def start_db():
    init_db()

app.include_router(q_router)
app.include_router(a_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8005)