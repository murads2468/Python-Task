
def analyze_transactions(transactions):

    customer_spending = {}
    transaction_ids = set()

    # Process transactions
    for transaction in transactions:

        # Check required keys
        required_keys = {"id", "customer", "category", "amount", "status"}

        if not isinstance(transaction, dict) or not required_keys.issubset(transaction):
            raise ValueError("Invalid transaction data")

        transaction_id = transaction["id"]
        customer = transaction["customer"]
        category = transaction["category"]
        amount = transaction["amount"]
        status = transaction["status"]

        # Reject duplicate transaction IDs
        if transaction_id in transaction_ids:
            raise ValueError("Duplicate transaction ID found")

        transaction_ids.add(transaction_id)

        # Validate transaction data
        if not isinstance(customer, str) or not customer.strip():
            raise ValueError("Invalid customer name")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Invalid category")

        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Invalid transaction amount")

        if status not in ("success", "failed"):
            raise ValueError("Invalid transaction status")

        # Add every customer, including failed-only customers
        if customer not in customer_spending:
            customer_spending[customer] = {}

        # Ignore failed transactions
        if status == "success":

            if category not in customer_spending[customer]:
                customer_spending[customer][category] = 0

            customer_spending[customer][category] += amount

    # Create customer report
    report = []

    for customer, categories in customer_spending.items():

        total = sum(categories.values())

        # Find top category
        if categories:
            top_category = sorted(
                categories.items(),
                key=lambda item: (-item[1], item[0])
            )[0][0]
        else:
            top_category = None

        report.append({
            "customer": customer,
            "total_spending": total,
            "top_category": top_category
        })

    # Sort by spending descending and customer name ascending
    report.sort(
        key=lambda item: (-item["total_spending"], item["customer"])
    )

    # Assign ranks (equal spending gets equal rank)
    previous_total = None
    rank = 0

    for position, item in enumerate(report, start=1):

        if item["total_spending"] != previous_total:
            rank = position

        item["rank"] = rank
        previous_total = item["total_spending"]

    return report


# Sample transactions
transactions = [
    {"id": 1, "customer": "Ali", "category": "Food",
     "amount": 500, "status": "success"},

    {"id": 2, "customer": "Ali", "category": "Travel",
     "amount": 200, "status": "failed"},

    {"id": 3, "customer": "Sara", "category": "Food",
     "amount": 700, "status": "success"}
]

# Display report
result = analyze_transactions(transactions)

for customer in result:
    print(customer)
