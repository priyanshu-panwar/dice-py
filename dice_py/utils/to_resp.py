"""
Converts a human readable command to a RESP command.
RESP Format:
    Simple Strings: A plain string prefixed with a +.
	Errors: A string prefixed with a -.
	Integers: Represented with a colon (:).
	Bulk Strings: Represented with a $ followed by the length and content.
	Arrays: Represented with an asterisk (*) followed by the number of elements.
"""


def to_resp(command: str) -> str:
    if not command:
        return "*1\r\n$0\r\n\r\n"
    parts = command.split()
    resp = f"*{len(parts)}\r\n"
    for part in parts:
        resp += f"${len(part)}\r\n{part}\r\n"
    return resp
