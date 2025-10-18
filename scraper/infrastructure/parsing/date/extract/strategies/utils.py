
from typing import Any



def _safe_str_strip(val: Any) -> str:
    if val is None:
        return ""
    try:
        return str(val).strip()
    except Exception:
        return ""
