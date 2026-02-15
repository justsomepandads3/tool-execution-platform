"""
Tool Registry.

This module maintains a simple registry of all available tools.
It's a manual registry (not auto-discovery) to keep it beginner-friendly and clear.

To add a new tool:
1. Create the tool class inheriting from BaseTool
2. Import it here
3. Add it to the TOOLS dictionary
"""

from app.tools.image_converter.tool import ImageConverterTool
from app.tools.image_compressor.tool import ImageCompressorTool
from app.tools.qr_generator.tool import QRGeneratorTool

# Dictionary of all available tools
# Key: tool name (lowercase, hyphens allowed)
# Value: instance of the tool class
TOOLS = {
    "qr-generator": QRGeneratorTool(),
    "image-converter": ImageConverterTool(),
    "image-compressor": ImageCompressorTool()
}


def get_tool(tool_name: str):
    """
    Get a tool by name from the registry.

    Args:
        tool_name: Name of the tool to retrieve

    Returns:
        The tool instance

    Raises:
        KeyError: If tool doesn't exist
    """
    if tool_name not in TOOLS:
        raise KeyError(f"Tool '{tool_name}' not found")
    return TOOLS[tool_name]


def list_tools():
    """
    Get metadata for all available tools.

    Returns:
        List of tool metadata dictionaries
    """
    return [tool.get_metadata() for tool in TOOLS.values()]


def tool_exists(tool_name: str) -> bool:
    """
    Check if a tool exists in the registry.

    Args:
        tool_name: Name of the tool

    Returns:
        True if tool exists, False otherwise
    """
    return tool_name in TOOLS
