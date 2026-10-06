from .analyzer import BRFAnalyzer

__version__ = "0.3.5"

__all__ = ["BRFAnalyzer", "__version__"]

# Registry is lazily imported to avoid circular dependencies
# Use: from brf.registry import REGISTRY_SOURCES, list_sources
