from src.transaction import transactions_summary

transactions = [7, 10, 36.8, 11, 200]
print(f"Transactions: {transactions} \n")
summary = transactions_summary(transactions)
print("Transactions Summary:", 
      "\nTotal:", summary["total"], 
      "\nAverage:", summary["average"], 
      "\nMaximum:", summary["maximum"], 
      "\nAbove Average Count:", summary["above_average_count"])