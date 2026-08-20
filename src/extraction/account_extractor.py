import re

IFSC_PATTERN = re.compile(r"\bIFSC\s*[:\-]?\s*([A-Z]{4}0[A-Z0-9]{6})\b", re.IGNORECASE)
ACCOUNT_NUMBER_PATTERN = re.compile(
    r"\b(?:A/?C\s*(?:NO|NUMBER)?|ACCOUNT\s*(?:NO|NUMBER)?)\s*[:\-]?\s*([0-9\-]{9,20})\b",
    re.IGNORECASE,
)
# More flexible name patterns
NAME_PATTERN = re.compile(
    r"\b(?:ACCOUNT\s*HOLDER\s*NAME|NAME|ACCOUNT\s*HOLDER|CUSTOMER\s*NAME)\s*[:\-]?\s*([A-Z][A-Za-z\s.]{2,50})",
    re.IGNORECASE | re.MULTILINE
)
BRANCH_PATTERN = re.compile(r"\bBRANCH\s*[:\-]?\s*([A-Za-z0-9 .,\-]{3,60})", re.IGNORECASE)


def extract_account_details(full_text):
    details = {
        "account_holder_name": None,
        "account_number": None,
        "ifsc_code": None,
        "branch": None,
    }

    # Extract IFSC
    ifsc_match = IFSC_PATTERN.search(full_text)
    if ifsc_match:
        details["ifsc_code"] = ifsc_match.group(1).upper()

    # Extract Account Number
    account_match = ACCOUNT_NUMBER_PATTERN.search(full_text)
    if account_match:
        details["account_number"] = account_match.group(1).replace("-", "")

    # Extract Name - try multiple approaches
    name_match = NAME_PATTERN.search(full_text)
    if name_match:
        raw_name = name_match.group(1).strip()
        # Clean up: take only the first line, remove extra spaces
        name_parts = raw_name.split('\n')[0].strip()
        # Remove trailing colons, numbers, or other junk
        name_cleaned = re.sub(r'[:\d]+$', '', name_parts).strip()
        if name_cleaned and len(name_cleaned) > 2:
            details["account_holder_name"] = name_cleaned
    
    # Fallback: Look for a name pattern without keyword (e.g., "John Smith" on its own line)
    # after account number but before transactions
    if not details["account_holder_name"]:
        # Look for capitalized name pattern (2-4 words starting with capitals)
        standalone_name = re.search(
            r'\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*\n',
            full_text
        )
        if standalone_name:
            details["account_holder_name"] = standalone_name.group(1).strip()

    # Extract Branch
    branch_match = BRANCH_PATTERN.search(full_text)
    if branch_match:
        details["branch"] = branch_match.group(1).strip().splitlines()[0].strip()

    return details
