import logging

logger = logging.getLogger(__name__)

class CalculatorEngine:
    def __init__(self, precision: int = 2):
        self.precision = precision
        logger.info("CalculatorEngine initialized.")

    def process_operation(self, a: float, b: float, operation: str) -> float:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return 0.0
            result = a / b
        else:
            raise ValueError(f"Unsupported operation: {operation}")
            
        return round(result, self.precision)