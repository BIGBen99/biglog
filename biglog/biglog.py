"""Module for logging messages with different levels and traceability."""
from datetime import datetime
import threading
import secrets
import inspect
import functools

LOG_LEVEL = {"level": "DEBUG"}  # Default log level stored in a dict

DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

def __log(level: str, message: str):
    """
    Logs a message to the console with a specific format.
    
    Args:
        level (str): The log level (DEBUG, INFO, WARNING, ERROR).
        message (str): The message to log.
    """
    print(
        datetime.now().isoformat().ljust(26),
        level.ljust(7),
        "[" + str(threading.get_ident()) + "|" + inspect.stack()[2].function.ljust(30) + "|" + __get_traceparent() + "]",
        message
    )

def __get_traceparent():
    """
    Retrieves the traceparent for the current thread.
    
    Returns:
        str: The traceparent string.
    """
    if not hasattr(__get_traceparent, "TRACEPARENT"):
        version = "00"
        trace_id = secrets.token_hex(16)
        parent_id = secrets.token_hex(8)
        trace_flags = "01"
        __get_traceparent.TRACEPARENT = version + \
            "-" + \
            trace_id + \
            "-" + \
            parent_id + \
            "-" + \
            trace_flags
    return __get_traceparent.TRACEPARENT

def set_log_level(level: str):
    """
    Sets the log level for the logger.
    
    Args:
        level (str): The log level to set (DEBUG, INFO, WARNING, ERROR).

    Raises:
        ValueError: If the log level is invalid.
    """
    if level in [DEBUG, INFO, WARNING, ERROR]:
        LOG_LEVEL["level"] = level
    else:
        raise ValueError("Invalid log level: " + level)

def debug(message: str):
    """
    Logs a debug message.
    
    Args:
        message (str): The message to log.
    """
    if LOG_LEVEL["level"] == DEBUG:
        __log(DEBUG, message)

def info(message: str):
    """
    Logs an informational message.
    
    Args:
        message (str): The message to log.
    """
    if LOG_LEVEL["level"] in [DEBUG, INFO]:
        __log(INFO, message)

def warning(message: str):
    """
    Logs a warning message.
    
    Args:
        message (str): The message to log.
    """
    if LOG_LEVEL["level"] in [DEBUG, INFO, WARNING]:
        __log(WARNING, message)

def error(message: str):
    """
    Logs an error message.
    
    Args:
        message (str): The message to log.
    """
    if LOG_LEVEL["level"] in [DEBUG, INFO, WARNING, ERROR]:
        __log(ERROR, message)

def log_entry_exit(func):
    """ Decorator to log entry and exit of a function, including parameters.
    This decorator logs the function name, parameters, and sensitive information"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        sensitive = {'password', 'token'}
        params = ', '.join(
            f"{name}={'****' if name.lower() in sensitive else repr(value)}"
            for name, value in bound.arguments.items()
        )
        debug(f"Entrée dans {func.__name__}({params})")
        result = func(*args, **kwargs)
        debug(f"Sortie de {func.__name__}")
        return result
    return wrapper