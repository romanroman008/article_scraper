import re

PL_MONTHS = {
    "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6,
    "lipca": 7, "sierpnia": 8, "września": 9, "wrzesnia": 9,
    "października": 10, "pazdziernika": 10, "listopada": 11, "grudnia": 12,
}
RX_DDMMYYYY = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
RX_PL_WORDS = re.compile(r"\b(\d{1,2})\s+([A-Za-ząćęłńóśźż]+)\s+(\d{4})\b", re.IGNORECASE)
