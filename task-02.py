
def longest_unique_window(text):

    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    char_index = {}
    start = 0
    longest_start = 0
    longest_length = 0

    for index, char in enumerate(text):

        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1

        char_index[char] = index

        window_length = index - start + 1

        if window_length > longest_length:
            longest_length = window_length
            longest_start = start

    substring = text[longest_start:longest_start + longest_length]

    return substring, longest_start, longest_length


# Test cases
print(longest_unique_window("abcabcbb"))
print(longest_unique_window(""))
print(longest_unique_window("pwwkew"))
print(longest_unique_window("abcdef"))
print(longest_unique_window("a b!a"))
