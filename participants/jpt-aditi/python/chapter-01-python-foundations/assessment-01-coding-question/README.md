## Assessment details- 
Participant:- Jyoti Prakash Thakur
GitHub username:- jpt-aditi
Learning area:- Python
Chapter:- Python and Machine Learning Foundations (Week 1)
Assessment title / number:- Coding Question

## Summary
This project implements the transaction summary utility that accepts a list of amounts and returns a summary containing:

- Total amount. 
- Average amount. 
- Maximum transaction. 
- Number of transactions above the average. 

The implementation is in `src/transaction.py` and includes a typed return contract using `TypedDict` for clearer return type expectations. It also validates invalid runtime inputs and raises a clear `TypeError` when non-numeric values are provided.

The tests are in `tests/test_transaction.py`. 

## How to run

1. Clone the repository and move into the project folder.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
3. Build and Run 

   ```bash
   python src/transaction.py
   ```
4. Test:

   ```bash
   python -m pytest -v
   ```


## Validation and results

- All tests passed successfully.
- The test suite reported: `5 passed in 0.01s`.

## Questions or known limitations 
None

## Submission checklist- 
[X] My work is in my participant folder under the correct chapter and assessment.  
[X] My assessment README includes setup and execution instructions.  
[X] I ran my code or restarted and ran all notebook cells successfully.  
[X] Required dependencies and references are documented. 
[X] I checked that the submission contains no credentials or restricted data.  
[X] I reviewed the changed files and removed unrelated changes.  
