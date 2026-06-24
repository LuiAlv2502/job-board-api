from fastapi import FastAPI, HTTPException, Depends
from database import init_db
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

@app.on_event("startup")
def on_startup() -> None:
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)