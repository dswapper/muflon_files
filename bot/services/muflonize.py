import re


def muflonize(text: str) -> str:
    allowed = re.compile(r'муф(?:л(?:о(?:н)?)?)?', re.IGNORECASE)
    result = []
    i = 0
    while i < len(text):
        if not text[i].isalpha():
            result.append(text[i])
            i += 1
            continue
        match = allowed.match(text, i)
        if match:
            result.append(text[i:match.end()])
            i = match.end()
        else:
            result.append('█')
            i += 1
    return ''.join(result)
