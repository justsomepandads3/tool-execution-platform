"""
Utility helper functions used across the application.

This module contains small utility functions for common tasks
that don't fit into a specific module.
"""

from typing import Any, Dict


def serialize_tool_output(output: Any) -> Dict[str, Any]:
    """
    Serialize tool output into a JSON-safe dictionary.

    Args:
        output: The output from a tool

    Returns:
        Dictionary with 'data' key containing the output
    """
    return {"data": output}


def create_error_response(error_message: str) -> Dict[str, str]:
    """
    Create a standardized error response.

    Args:
        error_message: The error message

    Returns:
        Dictionary with 'error' key
    """
    return {"error": error_message}
