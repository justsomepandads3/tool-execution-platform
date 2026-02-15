"""
Image Converter Tool.

This tool converts images between different formats (PNG, JPG, WebP, GIF, BMP).
It accepts an uploaded image file and returns the converted image.
"""

from loguru import logger

from app.core.base_tool import BaseTool
from app.core.exceptions import InvalidInputException, ToolExecutionException
from app.tools.image_converter.logic import convert_image
from app.tools.image_converter.schemas import ImageConverterInput


class ImageConverterTool(BaseTool):
    """
    Tool for converting images between different formats.

    This tool accepts an uploaded image and converts it to a specified format.
    Supported formats: PNG, JPG, JPEG, WebP, GIF, BMP
    """

    name = "image-converter"
    description = "Convert images between different formats"
    version = "1.0.0"
    output_type = "file"
    input_schema = {
        "type": "object",
        "properties": {
            "image_file_path": {
                "type": "file",
                "description": "Input image file (injected by API)"
            },
            "target_format": {
                "type": "string",
                "description": "Target image format",
                "enum": ["png", "jpg", "jpeg", "webp", "gif", "bmp"],
                "example": "png"
            },
            "quality": {
                "type": "integer",
                "description": "Quality for lossy formats (1-100)",
                "minimum": 1,
                "maximum": 100,
                "default": 85
            }
        },
        "required": ["image_file_path", "target_format"]
    }

    def run(self, **kwargs) -> tuple[str, str]:
        """
        Convert an image to a different format.

        Args:
            target_format: The target image format
            quality: Optional quality setting for lossy formats
            image_file_path: Path to the uploaded image file (injected by API)

        Returns:
            Tuple of (output_file_path, filename)

        Raises:
            InvalidInputException: If input validation fails
            ToolExecutionException: If conversion fails
        """
        logger.info("Image Converter tool started")

        # Extract image file path (set by API handler)
        image_file_path = kwargs.pop('image_file_path', None)
        if not image_file_path:
            raise ToolExecutionException("No image file provided")

        try:
            # Validate input
            input_data = ImageConverterInput(**kwargs)
            logger.info(f"Input validated: format={input_data.target_format}, quality={input_data.quality}")

        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            raise InvalidInputException(f"Invalid input: {str(e)}")

        try:
            # Convert image
            output_path, filename = convert_image(
                image_file_path,
                input_data.target_format,
                input_data.quality
            )
            logger.info(f"Image converted successfully: {filename}")
            return output_path, filename

        except Exception as e:
            logger.error(f"Image conversion failed: {str(e)}")
            raise ToolExecutionException(f"Failed to convert image: {str(e)}")
