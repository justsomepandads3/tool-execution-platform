"""
Base class for all tools in the platform.

Every tool must inherit from BaseTool and implement the required interface.
This ensures consistency and makes it easy to add new tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseTool(ABC):
    """
    Abstract base class that all tools must inherit from.

    Attributes:
        name: Unique identifier for the tool (lowercase, hyphens allowed)
        description: Human-readable description of what the tool does
        version: Semantic version of the tool
        input_schema: Dictionary describing input parameters in JSON Schema format
        output_type: Either "json" (returns JSON response) or "file" (returns FileResponse)
    """

    # These must be defined by subclasses
    name: str
    description: str
    version: str
    input_schema: Dict[str, Any]
    output_type: str  # "json" or "file"

    def __init__(self):
        """Initialize the tool and validate required attributes."""
        # Validate that required attributes are set
        if not hasattr(self, 'name') or not self.name:
            raise ValueError(f"{self.__class__.__name__} must define 'name' attribute")
        if not hasattr(self, 'description') or not self.description:
            raise ValueError(f"{self.__class__.__name__} must define 'description' attribute")
        if not hasattr(self, 'version') or not self.version:
            raise ValueError(f"{self.__class__.__name__} must define 'version' attribute")
        if not hasattr(self, 'input_schema') or not self.input_schema:
            raise ValueError(f"{self.__class__.__name__} must define 'input_schema' dict")
        if not hasattr(self, 'output_type') or self.output_type not in ("json", "file"):
            raise ValueError(f"{self.__class__.__name__} output_type must be 'json' or 'file'")

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool logic.

        This method must be implemented by subclasses.
        It receives the input parameters and returns the result.

        Args:
            **kwargs: Tool-specific input parameters

        Returns:
            For json output_type: Dictionary or data that will be JSON-serialized
            For file output_type: Tuple of (file_path: str, filename: str) or file_path: str

        Raises:
            ToolException: For tool-specific errors
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return tool metadata for the /api/tools endpoint.

        Returns:
            Dictionary containing tool information
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "input_schema": self.input_schema,
            "output_type": self.output_type,
        }
