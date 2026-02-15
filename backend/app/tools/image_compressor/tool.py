"""
Image Compressor Tool.

This tool compresses images to reduce file size while maintaining quality.
It accepts an uploaded image file and returns the compressed image.
"""
from loguru import logger

from app.core.base_tool import BaseTool
from app.core.exceptions import InvalidInputException, ToolExecutionException
from app.tools.image_compressor.logic import compress_image
from app.tools.image_compressor.schemas import ImageCompressorInput
from app.services.file_service import file_service

from fastapi import UploadFile

class ImageCompressorTool(BaseTool):
    """
    Tool for compressing images.

    This tool accepts an uploaded image and compresses it to reduce file size.
    Supported formats: PNG, JPG, JPEG, WebP, GIF, BMP
    """

    name = "image-compressor"
    description = "Compress images to reduce file size while maintaining quality"
    version = "1.0.0"
    output_type = "file"
    input_schema = {
        "type": "object",
        "properties": {
            "image_file_path": {
                "type": "file",
                "description": "Input Image file (injected by API)"
            },
            "quality": {
                "type": "integer",
                "description": "Quality for lossy formats (1-100)",
                "minimum": 1,
                "maximum": 100,
                "default": 85
            }
        },
        "required": ["image_file_path"]  # image_file_path is required, quality is optional
    }
    def run(self, **kwargs) -> tuple[str, str]:
        """
        Compress an image.

        Args:
            image: The uploaded image file (injected by API)
            quality: Quality level for compression (1-100) (optional, default=85)

        Returns:
            Tuple of (output_file_path, filename)

        Raises:
            InvalidInputException: If input parameters are invalid
            ToolExecutionException: If an error occurs during compression
        """
        logger.info("Image Compressor tool started")

        # Extract image file path (set by API handler)
        file_path = kwargs.get("image_file_path")
        if not file_path:
            raise ToolExecutionException("No image file provided")

        try:
            # Validate input
            logger.debug(f"Here is the file_path content: {file_path}\n\n\n")
            input_data = ImageCompressorInput(**kwargs)
            logger.info(f"Input validated: quality={input_data.quality}")

        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            raise InvalidInputException(f"Invalid input: {str(e)}")

        try:
            # Compress image
            output_path, filename = compress_image(
                file_path,
                input_data.quality
            )
            logger.info(f"Image compressed successfully: {filename}")
            return output_path, filename

        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            raise ToolExecutionException(f"Failed to compress image: {str(e)}")