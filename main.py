import csv
import argparse

from os.path import exists
from helpers import *

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="The path for the TSV transactions file")

args = parser.parse_args()
tsv_filepath = args.filepath
file_exists = exists(tsv_filepath)

if (not file_exists):
    print(f'`{tsv_filepath}` not found! ❌')
    exit(1)


def read_transactions_file(filepath):
    transactions = []
    CATEGORY = 0
    DESCRIPTION = 1
    DATE = 2
    COMMENTS = 3
    AMOUNT = 4

    with open(filepath) as file:
        tsv_reader = csv.reader(file, delimiter="\t", quotechar='"')

        # Skip the first row containing the headers
        next(tsv_reader)

        for row in tsv_reader:
            transactions.append({
                'category': row[CATEGORY],
                'description': row[DESCRIPTION],
                'date': row[DATE],
                'comments': row[COMMENTS],
                'amount': row[AMOUNT].replace(' EUR', '')
            })

    return transactions


def main():
    categories_to_filter_out = ['Ανακατανομή']
    transactions = read_transactions_file(tsv_filepath)

    # first transaction is in the last row of the tsv file, so it's the last element in the array
    first_transaction_date = transactions[-1]['date']
    month_of_first_transaction = first_transaction_date.split('/')[1]
    year_of_first_transaction = first_transaction_date.split('/')[2]

    # Only keep the transactions that belong to the same month as the first transaction made
    transactions[:] = [transaction for transaction in transactions if not belongs_to_different_month(
        transaction, month_of_first_transaction)]

    total_transactions = len(transactions)
    total_transactions_per_category = {}
    total_expenses_per_category = {}
    max_expense = -999999
    min_expense = 999999
    total_expenses = 0
    total_income = 0

    for transaction in transactions:
        category = transaction['category']
        amount = format_amount(transaction['amount'])

        if category not in categories_to_filter_out:
            if is_expense(amount):
                total_expenses += amount
                max_expense = amount if amount > max_expense else max_expense
                min_expense = amount if amount < min_expense else min_expense

                if total_expenses_per_category.get(category):
                    total_expenses_per_category[category] += amount
                else:
                    total_expenses_per_category[category] = amount
            else:
                total_income += amount

        if total_transactions_per_category.get(category):
            total_transactions_per_category[category] += 1
        else:
            total_transactions_per_category[category] = 1

    # min and max expenses are negative numbers, so min_expense is actually the max_expense and vice versa
    min_expense, max_expense = max_expense, min_expense
    total_expenses_per_category = {
        key: round(value, 2) for key, value in total_expenses_per_category.items()
    }

    print(f"No. of transactions: {total_transactions}")
    print(f"Total income: {round(total_income, 2)}")
    print(f"Total expenses: {round(total_expenses, 2)}")
    print(f"Max expense: {max_expense}")
    print(f"Min expense: {min_expense}")
    print(f"Transactions per category: {total_transactions_per_category}")
    print(f"Expenses per category: {total_expenses_per_category}")

    upload = input("\nUpload data to database? (Y/n)\n")

    if upload in ['y', 'Y', 'yes', '']:
        from db import connect_to_database, get_user_collection, insert_document

        print("Uploading... ⏳")

        db = connect_to_database()
        collection = get_user_collection(db)

        document = {
            "month": int(month_of_first_transaction),
            "year": int(year_of_first_transaction),
            "transactions": transactions,
            "total_transactions": total_transactions,
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "max_expense": max_expense,
            "min_expense": min_expense,
            "total_transactions_per_category": total_transactions_per_category,
            "total_expenses_per_category": total_expenses_per_category
        }

        record_id = insert_document(document, collection)

        if record_id:
            print('Data uploaded successfully! ✅')
        else:
            print("Upload failed. Please try again ❌")
    else:
        print("Exiting without upload...")
        exit(0)


main()
