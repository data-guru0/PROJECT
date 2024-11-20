from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def divide_numbers(a, b):
    try:
        result = a / b
        logger.info(f"Dividing {a} by {b}, result: {result}")
        return result
    except Exception as e:
        logger.error("Error in divide_numbers function")
        raise CustomException("Division by zero error", e)

if __name__ == "__main__":
    try:
        logger.info("Starting main program")
        divide_numbers(10, 0)
    except CustomException as ce:
        logger.error(str(ce))
    finally:
        logger.info("End of main program")
