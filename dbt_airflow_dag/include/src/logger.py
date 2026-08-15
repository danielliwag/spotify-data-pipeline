import logging
import json
import sys
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable
import os


class StructuredFormatter(logging.Formatter):
    """JSON-structured log formatter for production log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_data"):
            log_entry["data"] = record.extra_data

        # Add correlation ID if present (for distributed tracing)
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id

        return json.dumps(log_entry)


class ContextFilter(logging.Filter):
    """Add context fields to every log record."""

    def __init__(self, app_name: str = "spotify-pipeline"):
        super().__init__()
        self.app_name = app_name

    def filter(self, record: logging.LogRecord) -> bool:
        record.app = self.app_name
        return True


def get_logger(name: str, level: str = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)
        level: Log level from LOG_LEVEL env var, defaults to INFO

    Returns:
        Configured logger with structured output
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Console handler with structured JSON format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(StructuredFormatter())

    # Add context filter
    console_handler.addFilter(ContextFilter())

    logger.addHandler(console_handler)

    # Prevent propagation to root logger in Airflow
    logger.propagate = False

    return logger


class PipelineLogger:
    """
    Context-aware logger for pipeline operations with timing and metrics.
    """

    def __init__(self, name: str, correlation_id: str = None):
        self.logger = get_logger(name)
        self.correlation_id = correlation_id
        self._start_time = None

    def _log(self, level: int, message: str, **kwargs):
        """Log with optional extra data and correlation ID."""
        extra = {"extra_data": kwargs} if kwargs else {}
        if self.correlation_id:
            extra["correlation_id"] = self.correlation_id
        self.logger.log(level, message, extra=extra if extra else None)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, exc_info: bool = False, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
        if exc_info:
            self.logger.exception(message)

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def start_operation(self, operation: str) -> "PipelineLogger":
        """Mark the start of a timed operation."""
        self._start_time = datetime.now(timezone.utc)
        self.info(
            f"Starting {operation}",
            operation=operation,
            start_time=self._start_time.isoformat(),
        )
        return self

    def end_operation(self, operation: str, success: bool = True, **kwargs):
        """Mark the end of a timed operation with duration."""
        if self._start_time:
            duration_ms = int(
                (datetime.now(timezone.utc) - self._start_time).total_seconds() * 1000
            )
            self.info(
                f"Completed {operation}",
                operation=operation,
                success=success,
                duration_ms=duration_ms,
                **kwargs,
            )
            self._start_time = None
        else:
            self.info(f"Completed {operation}", success=success, **kwargs)


def log_execution(func: Callable) -> Callable:
    """
    Decorator to automatically log function entry/exit with timing.

    Usage:
        @log_execution
        def extract_data():
            ...
    """
    logger = get_logger(func.__module__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = datetime.now(timezone.utc)

        logger.debug(
            f"Entering {func_name}",
            extra={"extra_data": {"args_count": len(args), "kwargs": list(kwargs.keys())}},
        )

        try:
            result = func(*args, **kwargs)
            duration_ms = int(
                (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            )
            logger.info(
                f"Successfully completed {func_name}",
                extra={"extra_data": {"duration_ms": duration_ms, "success": True}},
            )
            return result

        except Exception as e:
            duration_ms = int(
                (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            )
            logger.error(
                f"Failed in {func_name}: {str(e)}",
                extra={
                    "extra_data": {
                        "duration_ms": duration_ms,
                        "error_type": type(e).__name__,
                        "success": False,
                    }
                },
            )
            raise

    return wrapper
