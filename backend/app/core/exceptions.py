"""
Custom exception classes for the Tool Execution Platform.

These exceptions are caught by the FastAPI exception handlers
and converted to appropriate HTTP responses.
"""


class ToolExecutionException(Exception):
    """
    Base exception for tool execution errors.

    This exception is raised when a tool fails to execute properly.
    The error message is safe to return to the client.
    """

    def __init__(self, message: str):
        """
        Initialize the exception.

        Args:
            message: Human-readable error message to return to client
        """
        self.message = message
        super().__init__(self.message)


class ToolNotFoundException(ToolExecutionException):
    """Raised when a requested tool does not exist."""

    pass


class InvalidInputException(ToolExecutionException):
    """Raised when tool input validation fails."""

    pass


class FileProcessingException(ToolExecutionException):
    """Raised when file upload or processing fails."""

    pass


class ToolValidationException(ToolExecutionException):
    """Raised when tool definition is invalid."""

    pass
