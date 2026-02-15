"""
Pydantic schemas for the QR Generator tool.

These schemas define the input/output structure for the tool.
"""

from pydantic import BaseModel, Field


class QRGeneratorInput(BaseModel):
    """Input schema for QR code generation."""

    data: str = Field(
        ...,
        description="Data to encode in QR code",
        min_length=1,
        max_length=2953,
        example="https://example.com"
    )


class QRGeneratorOutput(BaseModel):
    """Output schema for QR code generation."""

    message: str = Field(description="Success message")
    filename: str = Field(description="Generated filename")
