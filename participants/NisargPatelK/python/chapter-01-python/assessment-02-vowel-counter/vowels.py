def count_vowels(text):
    text = text.lower()
    vowels = "aeiou"
    c = 0
    for i in text:
        if i in vowels:
            c += 1
    return c


t = input("Enter a string: ")
vowel_count = count_vowels(t)
print(f"The number of vowels in '{t}' is: {vowel_count}")
