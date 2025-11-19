"""Custom exceptions for TOON converter."""


class TOONError(Exception):
    """Base exception for TOON converter."""
    pass


class TOONParseError(TOONError):
    """Raised when TOON parsing fails."""
    
    def __init__(self, message: str, line_number: int = None, column: int = None):
        self.message = message
        self.line_number = line_number
        self.column = column
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.line_number is not None:
            if self.column is not None:
                return f"Line {self.line_number}, Column {self.column}: {self.message}"
            return f"Line {self.line_number}: {self.message}"
        return self.message


class TOONValidationError(TOONError):
    """Raised when validation fails."""
    pass


class JSONValidationError(TOONError):
    """Raised when JSON validation fails."""
    pass
