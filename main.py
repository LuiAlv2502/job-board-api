from fastapi import FastAPI
from database import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)