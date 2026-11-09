# Python Vowel Counter

## Project Description

This Python program defines a reusable function named `count_vowels(text)` that counts the total number of vowels in a given string. It handles both uppercase and lowercase letters.

## Project Structure

```text
coding-question-2/
│
└── src/
    └── vowels_counter.py
```

## Python Code

The program uses:
- `def` to define a reusable function.
- `for` loop to iterate through each character in the string.
- `lower()` method to convert the string into lowercase.
- `if` condition to check whether a character is a vowel.
- A counter variable to calculate the total number of vowels.
- `return` to return the vowel count.

## How to Run the Program

1. Make sure Python is installed on your system.
2. Open the terminal in the `src` directory.
3. Execute the following command:

```bash
python vowels_counter.py
```

## Sample Input

```text
Enter string: Hello World
```

## Expected Output

```text
3
```

The output is `3` because "Hello World" contains three vowels: `e`, `o`, and `o`.

## Handling Uppercase and Lowercase Letters

The program uses the `lower()` method to convert the input string into lowercase before checking for vowels. This ensures that both uppercase and lowercase vowels are counted correctly.

For example:

```text
Enter string: SWARA
Output: 2
```

## Python Concepts Used

- Functions
- String Handling
- `for` Loop
- Conditional Statements
- `lower()` Method
- Counter Variable
- Return Statement
- User Input (`input()`)

## Conclusion

This program demonstrates how to create a reusable Python function to count vowels in a string while handling both uppercase and lowercase characters.