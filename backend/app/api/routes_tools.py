"""
Tool execution API routes.

These routes handle:
- Running tools with JSON input
- Running tools with file upload input
- Returning JSON or file responses appropriately
"""

from pathlib import Path
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from app.core.tool_registry import tool_exists, get_tool
from app.core.exceptions import (
    ToolNotFoundException,
    InvalidInputException,
    FileProcessingException,
    ToolExecutionException,
)
from app.services.file_service import file_service

router = APIRouter(prefix="/api/system/tools", tags=["tools"])


def get_media_type_and_extension(filename: str):
    """
    Determine the media type and extension from a filename.

    Args:
        filename: The output filename

    Returns:
        Tuple of (media_type, extension)
    """
    # Map of file extensions to media types
    MEDIA_TYPES = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf',
        '.json': 'application/json',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.zip': 'application/zip',
    }

    # Get extension from filename
    path = Path(filename)
    extension = path.suffix.lower()

    # Get media type or default to octet-stream
    media_type = MEDIA_TYPES.get(extension, 'application/octet-stream')

    return media_type, extension


@router.post("/{tool_name}/run")
async def run_tool(tool_name: str, request: Request):
    """
    Execute a tool with either JSON or multipart/form-data input.

    This endpoint is flexible and handles both:
    - application/json: JSON input body
    - multipart/form-data: File upload + form fields

    Args:
        tool_name: Name of the tool to run
        request: The HTTP request (used to detect content type)

    Returns:
        For json output_type: JSON response with data
        For file output_type: FileResponse with the file
    """
    logger.info(f"Tool execution requested: {tool_name}")

    # Check if tool exists
    if not tool_exists(tool_name):
        logger.warning(f"Tool not found: {tool_name}")
        raise ToolNotFoundException(f"Tool '{tool_name}' not found")

    tool = get_tool(tool_name)
    content_type = request.headers.get("content-type", "")

    try:
        # Parse input based on content type
        if "application/json" in content_type:
            logger.debug(f"Parsing JSON input for tool: {tool_name}")
            input_data = await request.json()
        elif "multipart/form-data" in content_type:
            logger.debug(f"Parsing multipart input for tool: {tool_name}")
            form_data = await request.form()
            input_data = {}

            # Process form fields
            for key, value in form_data.items():
                if isinstance(value, UploadFile):
                    # Handle file upload
                    logger.debug(f"Processing file upload: {value.filename}")
                    try:
                        content = await value.read()
                        file_path = file_service.save_uploaded_file(
                            content,
                            value.filename or "uploaded_file",
                            subfolder=tool_name
                        )
                        input_data[f"{key}_file_path"] = file_path
                        
                    except FileProcessingException as e:
                        logger.error(f"File processing failed: {str(e)}")
                        raise HTTPException(status_code=400, detail=str(e.message))
                else:
                    # Handle form field
                    input_data[key] = value

            # For image-converter, rename the file path
            if "image_file_path" in input_data:
                pass  # Already named correctly
            elif "file_file_path" in input_data:
                input_data["image_file_path"] = input_data.pop("file_file_path")
        else:
            raise HTTPException(
                status_code=400,
                detail="Content-Type must be application/json or multipart/form-data"
            )

        logger.debug(f"Input data: {list(input_data.keys())}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to parse request: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to parse request")

    # Execute tool
    try:
        logger.info(f"Executing tool: {tool_name}")
        result = tool.run(**input_data)
        logger.info(f"Tool execution successful: {tool_name}")

    except InvalidInputException as e:
        logger.warning(f"Invalid input for {tool_name}: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except FileProcessingException as e:
        logger.error(f"File processing error in {tool_name}: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except ToolExecutionException as e:
        logger.error(f"Tool execution error in {tool_name}: {e.message}")
        raise HTTPException(status_code=500, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error in {tool_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Tool execution failed")

    # Return result based on output type
    if tool.output_type == "json":
        logger.debug(f"Returning JSON response from {tool_name}")
        return {"data": result}

    elif tool.output_type == "file":
        # Result should be (file_path, filename)
        if isinstance(result, tuple) and len(result) == 2:
            file_path, filename = result
            logger.debug(f"Returning file response: {filename}")

            # Determine media type and extension from filename
            media_type, extension = get_media_type_and_extension(filename)

            logger.debug(f"File extension: {extension}, Media type: {media_type}")

            # Return file with appropriate media type and headers
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type=media_type,
                headers={
                    "X-File-Extension": extension,
                    "X-File-Name": filename,
                }
            )
        else:
            logger.error(f"Invalid file output format from {tool_name}")
            raise HTTPException(status_code=500, detail="Invalid tool output")

    else:
        logger.error(f"Unknown output_type for {tool_name}: {tool.output_type}")
        raise HTTPException(status_code=500, detail="Unknown output type")
