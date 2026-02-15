"""
Business logic for QR code generation.

This module contains the core logic for generating QR codes.
It's separated from the tool class to keep the code modular.
"""

import io
from pathlib import Path

import qrcode
from loguru import logger

from app.services.file_service import file_service


def generate_qr_code(data: str) -> tuple[str, str]:
    """
    Generate a QR code from the provided data.

    Args:
        data: String data to encode in QR code

    Returns:
        Tuple of (file_path, filename)

    Raises:
        Exception: If QR code generation fails
    """
    logger.info(f"Generating QR code for: {data[:50]}...")

    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=2,  # version 1 can hold up to 41 characters
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add data and optimize
        qr.add_data(data)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Generate filename
        filename = f"qr_code_{hash(data) % 10000000}.png"
        file_path, _ = file_service.generate_output_path(
            "qr_generator",
            filename,
            extension=".png"
        )

        # Save image
        img.save(file_path)

        logger.info(f"QR code generated: {file_path}")
        return file_path, filename

    except Exception as e:
        logger.error(f"QR code generation failed: {str(e)}")
        raise
