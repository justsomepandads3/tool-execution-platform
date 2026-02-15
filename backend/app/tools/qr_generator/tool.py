"""
QR Code Generator Tool.

This tool generates a QR code from text input and returns a PNG image file.
"""

from loguru import logger

from app.core.base_tool import BaseTool
from app.core.exceptions import InvalidInputException, ToolExecutionException
from app.tools.qr_generator.logic import generate_qr_code
from app.tools.qr_generator.schemas import QRGeneratorInput


class QRGeneratorTool(BaseTool):
    """
    Tool for generating QR codes from text input.

    This tool takes a string and generates a QR code image.
    The output is a PNG file that can be scanned by QR code readers.
    """

    name = "qr-generator"
    description = "Generate a QR code from text data"
    version = "1.0.0"
    output_type = "file"
    input_schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": "string",
                "description": "Data to encode in QR code",
                "minLength": 1,
                "maxLength": 2953,
                "example": "https://example.com"
            }
        },
        "required": ["data"]
    }

    def run(self, **kwargs) -> tuple[str, str]:
        """
        Generate a QR code.

        Args:
            data: String data to encode

        Returns:
            Tuple of (file_path, filename)

        Raises:
            InvalidInputException: If input validation fails
            ToolExecutionException: If QR generation fails
        """
        logger.info("QR Generator tool started")

        try:
            # Validate input
            input_data = QRGeneratorInput(**kwargs)
            logger.info(f"Input validated: data length = {len(input_data.data)}")

        except Exception as e:
            logger.error(f"Input validation failed: {str(e)}")
            raise InvalidInputException(f"Invalid input: {str(e)}")

        try:
            # Generate QR code
            file_path, filename = generate_qr_code(input_data.data)
            logger.info(f"QR code generated successfully: {filename}")
            return file_path, filename

        except Exception as e:
            logger.error(f"QR generation failed: {str(e)}")
            raise ToolExecutionException(f"Failed to generate QR code: {str(e)}")
