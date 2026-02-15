"""
System API routes.

These routes provide system-level information:
- Health check
- Tool listing
- Single tool metadata
"""

from fastapi import APIRouter
from loguru import logger

from app.core.tool_registry import list_tools, tool_exists, get_tool
from app.core.exceptions import ToolNotFoundException

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns:
        {"status": "ok"}
    """
    logger.debug("Health check requested")
    return {"status": "ok"}


@router.get("/tools")
def list_all_tools():
    """
    List all available tools with their metadata.

    Returns:
        List of tool metadata dictionaries
    """
    logger.info("Listing all tools")
    tools = list_tools()
    return {"tools": tools, "count": len(tools)}


@router.get("/tools/{tool_name}")
def get_tool_metadata(tool_name: str):
    """
    Get metadata for a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Tool metadata dictionary

    Raises:
        ToolNotFoundException: If tool doesn't exist
    """
    logger.info(f"Getting metadata for tool: {tool_name}")

    if not tool_exists(tool_name):
        logger.warning(f"Tool not found: {tool_name}")
        raise ToolNotFoundException(f"Tool '{tool_name}' not found")

    tool = get_tool(tool_name)
    return tool.get_metadata()
