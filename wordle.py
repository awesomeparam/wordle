from collections import Counter
from collections import defaultdict
import string
import re

def find_words_with_letters(word_list, required_letters):
    result = []
    for word in word_list:
        if all(letter in word for letter in required_letters):
            result.append(word)
    return result

def find_words_not_with_letters(word_list, excluded_letters):
    return [
        word for word in words
        if not any(char in excluded_chars for char in word)
    ]

def filter_words(word_list,set1,set2):

    result5 = []
    result4 = []
    result3 = []
    result2 = []
    result1 = []

    for word in word_list:
        count_set1 = sum(1 for ch in word if ch in set1)
        count_set2 = sum(1 for ch in word if ch in set2)

        if count_set1 >= 5 and count_set2 == 0:
            result5.append(word)
            continue

        if count_set1 >= 4 and count_set2 >= 0:
            result4.append(word)
            continue
            
        if count_set1 >= 3 and count_set2 >= 0:
            result3.append(word)
            continue

        if count_set1 >= 2 and count_set2 >= 0:
            result2.append(word)
            continue

        if count_set1 >= 1 and count_set2 >= 0:
            result1.append(word)
            
    if len(result5) > 0:
        return result5

    if len(result4) > 0:
        return result4

    if len(result3) > 0:
        return result3

    if len(result2) > 0:
        return result2

    return result1
 
wordlist_path = "flwords.txt"  # Ensure this file is in the same folder as your script

# Accept input for characters to omit
omit_chars = input("Enter characters to omit (no spaces): ").lower()
excluded_chars = set(omit_chars)

# Accept input for characters to include
incl_chars = input("Enter characters to include (no spaces): ").lower()
required_letters = set(incl_chars)

pattern_input = input("Enter a regular expression pattern: ")
pattern1 = re.compile(pattern_input, re.IGNORECASE)

# Read all words
with open(wordlist_path, "r") as file:
    words = file.read().splitlines()

# Get matching words
rslt_words = find_words_with_letters(words, required_letters)

# Filter words
filtered_words = [word for word in rslt_words if not any(char in excluded_chars for char in word)]
   

result_words = [word for word in filtered_words if pattern1.match(word)]

if len(result_words) == 1:
    print ("Result: ", result_words[0])
    exit(0)

# Dictionary to count character occurrences (once per word)
char_counts = defaultdict(int)

# Output
print("5-letter words using only the allowed letters:")
for word in sorted(result_words):
    print(word)
    
    unique_chars = set(word)
    for char in unique_chars:
        if char not in required_letters:
           char_counts[char] += 1

# Sort by occurrence count in descending order
sorted_items = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

# Display results
print("\nCharacter occurrence counts (one count per word):")
setchars = []
for char, count in sorted_items:
    print(f"{char}: {count}")
    setchars.append(char)
    
# Step 4: Create a set of sorted 
set1 = {char for char, _ in sorted_items}
print("Words choices for ")
print(setchars)
print("to try on wordle: ")

rslt_words = filter_words(words,set1,required_letters)

# Output
for word in sorted(rslt_words):
    print(word)
