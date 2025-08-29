import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def start_db():
    init_db()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8005)