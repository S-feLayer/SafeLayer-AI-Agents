from .redact_per_pdf import redact_pdf
from .redact_text import redact_text
from .redact_code import redact_code_file
from .redact_content import redact_content, get_supported_formats
from .ai_privacy_shield import DataGuardPrivacyShield, DataGuardEnterprisePrivacyAPI
from .enhanced_detection import EnhancedDetection
from .advanced_masking import AdvancedMasking, MaskingStrategy

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("dataguard")
except ImportError:
    __version__ = "unknown"

__all__ = [
    "redact_pdf",
    "redact_text", 
    "redact_code_file",
    "redact_content",
    "get_supported_formats",
    "DataGuardPrivacyShield",
    "DataGuardEnterprisePrivacyAPI",
    "EnhancedDetection",
    "AdvancedMasking",
    "MaskingStrategy"
]
