"""
File service for handling file uploads and temporary file management.

This module provides utilities for:
- Saving uploaded files securely
- Validating file sizes
- Cleaning filenames
- Managing temporary directories
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple

from loguru import logger

from app.core.config import settings
from app.core.exceptions import FileProcessingException


class FileService:
    """
    Service for managing file uploads and temporary files.

    This class handles:
    - Creating and managing the temporary directory
    - Saving uploaded files with validation
    - Cleaning filenames to prevent directory traversal
    - Handling file cleanup
    """

    def __init__(self):
        """Initialize the file service and ensure temp directory exists."""
        self.temp_dir = Path(settings.TEMP_DIR)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileService initialized with temp_dir: {self.temp_dir}")

    def clean_filename(self, filename: str) -> str:
        """
        Clean filename to prevent directory traversal attacks.

        Removes dangerous characters and path separators.
        Keeps only alphanumeric, dots, hyphens, and underscores.

        Args:
            filename: Original filename

        Returns:
            Cleaned filename safe for filesystem

        Raises:
            FileProcessingException: If filename is invalid or dangerous
        """
        if not filename:
            raise FileProcessingException("Filename cannot be empty")

        # Remove path separators and parent directory references
        filename = filename.replace("\\", "").replace("/", "")
        filename = filename.replace("..", "")

        # Keep only safe characters: alphanumeric, ., -, _
        safe_filename = re.sub(r'[^\w\-.]', '', filename)

        if not safe_filename:
            raise FileProcessingException("Filename contains no valid characters")

        return safe_filename

    def validate_file_size(self, file_size: int) -> None:
        """
        Validate that file size is within limits.

        Args:
            file_size: Size of file in bytes

        Raises:
            FileProcessingException: If file exceeds max size
        """
        if file_size > settings.MAX_FILE_SIZE:
            size_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
            raise FileProcessingException(
                f"File size exceeds maximum of {size_mb}MB"
            )

    def save_uploaded_file(
        self,
        file_content: bytes,
        original_filename: str,
        subfolder: Optional[str] = None
    ) -> str:
        """
        Save an uploaded file to the temporary directory.

        Args:
            file_content: Binary content of the file
            original_filename: Original filename from upload
            subfolder: Optional subfolder to organize files

        Returns:
            Path to saved file

        Raises:
            FileProcessingException: If file cannot be saved
        """
        try:
            # Validate file size
            self.validate_file_size(len(file_content))

            # Clean filename
            clean_name = self.clean_filename(original_filename)

            # Determine save path
            if subfolder:
                save_dir = self.temp_dir / subfolder
                save_dir.mkdir(parents=True, exist_ok=True)
            else:
                save_dir = self.temp_dir

            # Save file
            file_path = save_dir / clean_name
            file_path.write_bytes(file_content)

            logger.info(f"File saved: {file_path}")
            return str(file_path)

        except FileProcessingException:
            raise
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            raise FileProcessingException(f"Failed to save file: {str(e)}")

    def generate_output_path(
        self,
        tool_name: str,
        filename: str,
        extension: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Generate a path for output files.

        Args:
            tool_name: Name of the tool generating the file
            filename: Base filename
            extension: File extension (without dot)

        Returns:
            Tuple of (full_path, filename_with_ext)
        """
        # Create tool-specific output directory
        output_dir = self.temp_dir / tool_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean filename
        clean_name = self.clean_filename(filename)

        # Add extension if provided
        if extension:
            if not extension.startswith('.'):
                extension = '.' + extension
            filename_with_ext = clean_name + extension
        else:
            filename_with_ext = clean_name

        output_path = output_dir / filename_with_ext
        return str(output_path), filename_with_ext

    def cleanup_temp_files(self, max_age_hours: int = 24) -> None:
        """
        Clean up old temporary files (optional).

        This can be called periodically to clean old files.
        Currently kept simple without automatic cleanup.

        Args:
            max_age_hours: Only remove files older than this (not implemented yet)
        """
        # Simple implementation: just log
        logger.info("Temp directory cleanup requested")
        # You can extend this later to actually delete old files


# Create a global instance
file_service = FileService()
