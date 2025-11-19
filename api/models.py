"""Pydantic models for API."""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Union


class ConvertRequest(BaseModel):
    """Request model for conversion."""
    data: Union[Dict[str, Any], List[Any], str] = Field(..., description="Data to convert")
    indent: int = Field(2, description="Indentation spaces", ge=1, le=8)


class ConvertResponse(BaseModel):
    """Response model for conversion."""
    result: str = Field(..., description="Converted data")
    format: str = Field(..., description="Output format (json or toon)")


class ValidateRequest(BaseModel):
    """Request model for validation."""
    data: str = Field(..., description="Data to validate")


class ValidateResponse(BaseModel):
    """Response model for validation."""
    valid: bool = Field(..., description="Whether data is valid")
    error: str = Field("", description="Error message if invalid")
    details: Dict[str, Any] = Field(default_factory=dict, description="Error details")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional error details")
