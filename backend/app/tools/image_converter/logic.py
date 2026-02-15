"""
Business logic for image conversion.

This module contains the core logic for converting images between formats.
It handles Pillow operations safely with proper error handling.
"""

from pathlib import Path

from loguru import logger
from PIL import Image

from app.core.config import settings
from app.services.file_service import file_service


def convert_image(
    input_path: str,
    target_format: str,
    quality: int = 100
) -> tuple[str, str]:
    """
    Convert an image to a different format.

    Args:
        input_path: Path to the input image file
        target_format: Target format (png, jpg, jpeg, webp, gif, bmp)
        quality: Quality for lossy formats (1-100)

    Returns:
        Tuple of (output_path, filename)

    Raises:
        Exception: If conversion fails
    """
    logger.info(f"Converting image: {input_path} to {target_format}")

    try:
        # Validate target format
        allowed_formats = settings.ALLOWED_IMAGE_FORMATS
        if target_format.lower() not in allowed_formats:
            raise ValueError(f"Format {target_format} not allowed")

        # Open image
        image = Image.open(input_path.file)

        # Convert RGBA to RGB if needed for JPEG
        if target_format.lower() in ('jpg', 'jpeg') and image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # Generate output filename
        output_name = f"converted_{hash(input_path.filename) % 10000000}"
        output_path, filename = file_service.generate_output_path(
            "image_converter",
            output_name,
            extension=f".{target_format.lower()}"
        )

        # Save converted image
        if target_format.lower() in ('jpg', 'jpeg', 'webp'):
            image.save(output_path, format=target_format.upper(), quality=quality)
        else:
            image.save(output_path, format=target_format.upper())

        logger.info(f"Image converted successfully: {output_path}")
        return output_path, filename

    except Exception as e:
        logger.error(f"Image conversion failed: {str(e)}")
        raise
