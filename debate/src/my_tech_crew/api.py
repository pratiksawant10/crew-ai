#!/usr/bin/env python
import sys
import warnings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from my_tech_crew.crew import MyTechCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI()

class DebateInput(BaseModel):
    motion: str = "There should be a law that all cars must be electric"

class TrainInput(BaseModel):
    topic: str = "AI LLMs"
    n_iterations: int
    filename: str
    current_year: str = str(datetime.now().year)

class ReplayInput(BaseModel):
    task_id: str

class TestInput(BaseModel):
    topic: str = "AI LLMs"
    n_iterations: int
    eval_llm: str
    current_year: str = str(datetime.now().year)

@app.post("/run")
async def run(input_data: DebateInput):
    """
    Run the crew via API.
    """
    try:
        result = MyTechCrew().crew().kickoff(inputs=input_data.dict())
        return {"result": result.raw}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while running the crew: {str(e)}")

@app.post("/train")
async def train(input_data: TrainInput):
    """
    Train the crew via API.
    """
    try:
        MyTechCrew().crew().train(
            n_iterations=input_data.n_iterations,
            filename=input_data.filename,
            inputs=input_data.dict(exclude={'n_iterations', 'filename'})
        )
        return {"status": "Training completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while training the crew: {str(e)}")

@app.post("/replay")
async def replay(input_data: ReplayInput):
    """
    Replay the crew execution via API.
    """
    try:
        result = MyTechCrew().crew().replay(task_id=input_data.task_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while replaying the crew: {str(e)}")

@app.post("/test")
async def test(input_data: TestInput):
    """
    Test the crew execution via API.
    """
    try:
        result = MyTechCrew().crew().test(
            n_iterations=input_data.n_iterations,
            eval_llm=input_data.eval_llm,
            inputs=input_data.dict(exclude={'n_iterations', 'eval_llm'})
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while testing the crew: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)