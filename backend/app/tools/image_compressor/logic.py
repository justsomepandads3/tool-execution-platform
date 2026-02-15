"""
Business logic for image compression.

This module contains the core logic for compressing images.
It handles Pillow operations safely with proper error handling.
"""
from loguru import logger
from PIL import Image
from app.services.file_service import file_service

import os
def compress_image(
    input_path: str,
    quality: int = 70
) -> tuple[str, str]:
    """
    Compress an image by reducing its quality.

    Args:
        input_path: Path to the input image file
        quality: Quality for lossy formats (1-100) (optional, default=85)

    Returns:
        Tuple of (output_path, filename)
    """
    

    logger.info(f"Compressing image: {input_path} with quality={quality}")

    try:
        image_stream = input_path.file
        # Open image
        image = Image.open(image_stream)
        
        # Convert to RGB (needed for PNGs with alpha)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Generate output filename
        file_name, ext = os.path.splitext(input_path.filename)
        output_name = f"compressed_{hash(file_name) % 10000000}{ext}"
        output_path, filename = file_service.generate_output_path(
            f"{file_name}",
            output_name,
            extension=ext
        )

        # Save compressed image
        image.save(output_path, quality=quality, optimize=True, format=ext.strip("."))

        return output_path, filename

    except Exception as e:
        logger.error(f"Error compressing image: {e}")
        raise e