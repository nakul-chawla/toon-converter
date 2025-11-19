"""FastAPI application for TOON converter."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from toon_converter import (
    json_to_toon,
    toon_to_json,
    validate_json,
    validate_toon,
    get_error_details
)
from .models import (
    ConvertRequest,
    ConvertResponse,
    ValidateRequest,
    ValidateResponse,
    ErrorResponse
)

app = FastAPI(
    title="TOON Converter API",
    description="Convert between JSON and TOON (Token-Oriented Object Notation) formats",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "TOON Converter API",
        "version": "0.1.0",
        "endpoints": {
            "convert": {
                "json_to_toon": "/convert/json-to-toon",
                "toon_to_json": "/convert/toon-to-json"
            },
            "validate": {
                "json": "/validate/json",
                "toon": "/validate/toon"
            }
        }
    }


@app.post("/convert/json-to-toon", response_model=ConvertResponse)
async def convert_json_to_toon(request: ConvertRequest):
    """Convert JSON to TOON format."""
    try:
        result = json_to_toon(request.data, indent=request.indent)
        return ConvertResponse(result=result, format="toon")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error": str(e), "details": get_error_details(e)}
        )


@app.post("/convert/toon-to-json", response_model=ConvertResponse)
async def convert_toon_to_json(request: ValidateRequest):
    """Convert TOON to JSON format."""
    try:
        data = toon_to_json(request.data)
        result = json.dumps(data, indent=2)
        return ConvertResponse(result=result, format="json")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"error": str(e), "details": get_error_details(e)}
        )


@app.post("/validate/json", response_model=ValidateResponse)
async def validate_json_endpoint(request: ValidateRequest):
    """Validate JSON format."""
    try:
        is_valid, error = validate_json(request.data)
        details = {}
        if not is_valid:
            try:
                json.loads(request.data)
            except json.JSONDecodeError as e:
                details = get_error_details(e)
        
        return ValidateResponse(valid=is_valid, error=error, details=details)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )


@app.post("/validate/toon", response_model=ValidateResponse)
async def validate_toon_endpoint(request: ValidateRequest):
    """Validate TOON format."""
    try:
        is_valid, error = validate_toon(request.data)
        return ValidateResponse(valid=is_valid, error=error)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": str(e)}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
