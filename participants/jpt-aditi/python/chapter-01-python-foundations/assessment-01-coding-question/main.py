from src.transaction import transactions_summary

transactions = [7, 10, 36.8, 11, 200]
print(f"Transactions: {transactions} \n")
summary = transactions_summary(transactions)
print("Transactions Summary:")
print(f"Total: {summary['total']:,.2f}")
print(f"Average: {summary['average']:,.2f}")
print(f"Maximum: {summary['maximum']}")
print(f"Above Average Count: {summary['above_average_count']}")