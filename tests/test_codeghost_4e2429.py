from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from apps.financial_calculator.services.calculator_service import CalculatorEngine

app = FastAPI()
engine = CalculatorEngine()

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str

@app.post("/calculate")
async def calculate_endpoint(req: CalculationRequest):
    return {"result": engine.process_operation(req.a, req.b, req.operation)}

def test_reproduce_crash():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post("/calculate", json={"a": 10, "b": 0, "operation": "divide"})
    assert response.status_code != 500