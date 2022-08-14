def belongs_to_different_month(transaction, month):
    transaction_month = transaction['date'].split('/')[1]

    return transaction_month != month


def is_expense(amount):
    return amount < 0


def format_amount(amount):
    if '.' in amount:  # e.g. 2.500,00
        amount = amount.replace('.', '').replace(',', '.')
    else:  # e.g. 23,50
        amount = amount.replace(',', '.')

    return float(amount)
