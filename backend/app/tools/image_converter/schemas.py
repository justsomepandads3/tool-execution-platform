"""
Pydantic schemas for the Image Converter tool.

These schemas define the input/output structure for the tool.
"""

from pydantic import BaseModel, Field
from fastapi import UploadFile


class ImageConverterInput(BaseModel):
    """Input schema for image conversion."""
    image_file_path: UploadFile = Field(
        description="Input image file (injected by API)"
    ),
    target_format: str = Field(
        ...,
        description="Target image format",
        pattern="^(png|jpg|jpeg|webp|gif|bmp)$",
        example="png"
    )
    quality: int = Field(
        default=85,
        ge=1,
        le=100,
        description="Quality for lossy formats (JPEG, WebP)"
    )


class ImageConverterOutput(BaseModel):
    """Output schema for image conversion."""

    message: str = Field(description="Success message")
    filename: str = Field(description="Converted filename")
    format: str = Field(description="Output format")
