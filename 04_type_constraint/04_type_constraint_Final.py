
from typing import Final

# Final


# ------------------------------------------------------------------------------
# variables can not be modified
# ------------------------------------------------------------------------------

x: Final[int] = 5

x = 3


# ----------
VENDOR_NAME: Final = "Viafore's Auto-Dog"

vendor_info = "Auto-Dog v1.0"
vendor_info += VENDOR_NAME

VENDOR_NAME += VENDOR_NAME
 