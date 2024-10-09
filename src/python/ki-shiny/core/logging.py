# core/logging.py


import functools
import time

from loguru import logger

# Set up logging to a file
logger.add(
    "logs/debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB"
)

RED_COLOR = "\033[91m"
RESET_COLOR = "\033[39m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"


def truncate_string(s, max_length=200):
    return s if len(s) <= max_length else s[:max_length] + "..."


# Decorator for logging function calls
def log_function_call(log_level="info"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log the function call with arguments

            # Convert the result to a string and truncate if necessary
            args_str = truncate_string(str(args))
            kwargs_str = truncate_string(str(kwargs))

            log_message = f"{CYAN}START {func.__name__}:{RESET_COLOR} args: {args_str}, kwargs: {kwargs_str}"
            getattr(logger, log_level)(log_message)

            start_time = time.time()  # Track start time

            try:
                # Execute the function
                result = func(*args, **kwargs)

                # Convert the result to a string and truncate if necessary
                result_str = truncate_string(str(result))

                # Log the result
                execution_time = time.time() - start_time
                execution_time_str = (
                    f"{YELLOW}{execution_time:.4f} seconds{RESET_COLOR}"
                )

                getattr(logger, log_level)(
                    f"{CYAN}RETURNED {func.__name__}:{RESET_COLOR} {result_str} in {execution_time_str}"
                )

                return result

            except Exception as e:
                # Log any exception that occurs
                logger.error(f"Exception in function {func.__name__}: {e}")
                raise

        return wrapper

    return decorator
