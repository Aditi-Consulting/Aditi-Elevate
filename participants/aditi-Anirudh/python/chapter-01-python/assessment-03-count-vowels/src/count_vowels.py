def vowels_count(string):
    """
    Count the number of vowels in a given string.

    Parameters:
    string (str): The input string to count vowels in.

    Returns:
    int: The number of vowels in the string.
    """
    if not isinstance(string, str):
        raise ValueError("Input must be a string.")
    try:
        str_lower = string.lower()
        vowels = "aeiouAEIOU"
        count = 0
        for char in str_lower:
            if char in vowels:
                count += 1
    except AttributeError:
        return 0
    return count
print(vowels_count("Hello World!"))  # Example usage


