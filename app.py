import uvicorn
from fastapi import FastAPI

from db.session import init_db

app = FastAPI()

@app.on_event("startup")
def start_db():
    init_db()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8005)