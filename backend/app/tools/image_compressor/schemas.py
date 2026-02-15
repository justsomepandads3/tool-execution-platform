"""
Pydantic schemas for the Image Compressor tool.

These schemas define the input/output structure for the tool.
"""

from pydantic import BaseModel, Field
from fastapi import UploadFile

class ImageCompressorInput(BaseModel):
    """Input schema for image compression."""
    image_file_path: UploadFile = Field(
        description="Input image file (injected by API)"
    ),
    quality: int = Field(
        default=75,
        ge=1,
        le=100,
        description="Quality level for compression (1-100)"
    )

class ImageCompressorOutput(BaseModel):
    """Output schema for image compression."""

    message: str = Field(description="Success message")
    filename: str = Field(description="Compressed filename")
    quality: int = Field(description="Applied quality level")
