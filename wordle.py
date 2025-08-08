import re
from collections import defaultdict
from typing import List, Set


def load_word_list(path: str) -> List[str]:
    """Load words from a file and return only 5-letter lowercase words."""
    with open(path, "r") as file:
        return [word.lower() for word in file.read().splitlines()]


def get_user_input() -> tuple[Set[str], Set[str], re.Pattern]:
    """Get characters to include, exclude, and regex pattern from the user."""
    print("Enter characters to omit (no spaces):")
    omit_chars = input("> ").strip().lower()

    print("Enter characters to include (no spaces):")
    incl_chars = input("> ").strip().lower()

    print("Enter a regular expression pattern (e.g., ^a.... for words starting with 'a'):")
    pattern_input = input("> ").strip()

    excluded_chars = set(omit_chars)
    required_chars = set(incl_chars)
    pattern = re.compile(pattern_input, re.IGNORECASE)

    return required_chars, excluded_chars, pattern


def filter_required_letters(words: List[str], required_letters: Set[str]) -> List[str]:
    """Return words that contain all required letters."""
    return [word for word in words if required_letters.issubset(set(word))]


def filter_excluded_letters(words: List[str], excluded_letters: Set[str]) -> List[str]:
    """Return words that do not contain any excluded letters."""
    return [word for word in words if not set(word) & excluded_letters]


def match_pattern(words: List[str], pattern: re.Pattern) -> List[str]:
    """Return words that match a regex pattern."""
    return [word for word in words if pattern.match(word)]


def count_character_occurrences(words: List[str], exclude: Set[str]) -> dict:
    """
    Count how many words contain each character (excluding required ones).
    Each character is counted once per word.
    """
    counts = defaultdict(int)
    for word in words:
        for char in set(word):
            if char not in exclude:
                counts[char] += 1
    return counts


def filter_by_letter_frequency(words: List[str], freq_letters: Set[str], required_letters: Set[str]) -> List[str]:
    """
    Return the best candidate words based on how many frequent letters they include,
    excluding required letters.
    """
    buckets = {5: [], 4: [], 3: [], 2: [], 1: []}

    for word in words:
        set_word = set(word)
        count_freq = len(set_word & freq_letters)

        for n in range(5, 0, -1):
            if count_freq >= n:
                buckets[n].append(word)
                break

    for n in range(5, 0, -1):
        if buckets[n]:
            return buckets[n]

    return []


def main():
    WORDLIST_PATH = "flwords.txt"

    print("Loading words...")
    words = load_word_list(WORDLIST_PATH)
    print(f"{len(words)} words loaded.\n")

    required_letters, excluded_letters, pattern = get_user_input()
    print("\nFiltering words...\n")

    # Apply filters
    filtered = filter_required_letters(words, required_letters)
    filtered = filter_excluded_letters(filtered, excluded_letters)
    filtered = match_pattern(filtered, pattern)

    if not filtered:
        print("No matching words found.")
        exit(1)

    if len(filtered) == 1:
        print ("Result: ", filtered[0])
        exit(0)

    
    # ✅ Print filtered words
    print("5-letter words using only the allowed letters:")
    for word in sorted(filtered):
        print(word)

    # Step 4: Count character occurrences
    char_counts = count_character_occurrences(filtered, required_letters)

    # Display character frequencies
    print("\nCharacter occurrence counts (excluding required letters):")
    sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_chars:
        print(f"{char}: {count}")

    # Step 5: Suggest best words using letter frequency
    freq_letter_set = {char for char, _ in sorted_chars}

    suggested_words = filter_by_letter_frequency(words, freq_letter_set, required_letters)

    # Output suggestions
    print("\nSuggested words to try:")
    for word in sorted(suggested_words):
        print(word)


if __name__ == "__main__":
    main()
