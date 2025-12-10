class BomerError(Exception):
    """Base exception for all Bomer-related errors."""
    pass

class ConfigError(BomerError):
    """Raised when bomer.yaml is missing or invalid."""
    pass


class InputFileError(BomerError):
    """Raised when BOM or supplier inputs are invalid."""
    pass
