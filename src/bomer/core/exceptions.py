class BomerError(Exception):
    """Base exception for all Bomer-related errors."""
    pass


class ConfigError(BomerError):
    """Raised when bomer.yaml is invalid or inconsistent."""
    pass


class BomLoadError(BomerError):
    """Raised when the BOM file cannot be loaded."""
    pass


class SupplierLoadError(BomerError):
    """Raised when supplier data cannot be loaded."""
    pass
