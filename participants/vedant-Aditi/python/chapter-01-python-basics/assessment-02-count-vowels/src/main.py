def count_vowels(text):
    vowels = "aeiou"
    count = 0

    for character in text:
        if character.lower() in vowels:
            count += 1

    return count


if __name__ == "__main__":
    sample_text = input("Enter text: ")
    print(count_vowels(sample_text))
