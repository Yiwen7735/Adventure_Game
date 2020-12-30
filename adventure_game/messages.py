def get_a_or_an(s: str) -> str:
    """
    Determines whether the singular counter for a string should be 'a' or 'an'.

    Args:
        s: The string to analyze.

    Returns:
        'an' if s starts with a vowel sound, 'a' otherwise.

    """
    if any(s.startswith(c) for c in ['a', 'e', 'i', 'o', 'u', 'honor']):
        return 'an'
    return 'a'
