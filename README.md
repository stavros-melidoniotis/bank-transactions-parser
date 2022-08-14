# bank-transactions-parser
Python script that parses bank account transactions, extracts useful analytics and stores them to MongoDB.

# How to use
Clone the repository, navigate to the project directory and install all the required modules by typing ```pip install -r requirements.txt```. For the database upload feature to work you must also create a ```.env``` file within the project directory and define the following variables:

1) ```MONGODB_URL```
2) ```MONGODB_USER```
3) ```MONGODB_PASSWORD```
4) ```MONGODB_COLLECTION```

To run the script you simply type ```python main.py path/to/tsv/file```. 

**IMPORTANT:**

- The script only supports transactions that are exported from Piraeus Bank. If you're interested in supporting more banks create a Pull Request and I'll be happy to include it.
- The script expects that all the transactions inside the ```tsv``` file belong to the same month e.g. transactions from 01/07 - 31/07. If you export the transactions from different months the analytics produced will not be correct.

# How to export transactions
Login to your winbank account and find the transactions of the account you're interested in. Export the transactions as a ```txt``` file. The next step is to change the file's extensions to ```tsv``` and open it on your preferred text editor. When you open the file make sure to delete any text before and after the transactions table and save it. The final ```tsv``` file should look like this:

| Κατηγορία  | Περιγραφή Συναλλαγής | Ημ/νία Συναλλαγής | Σχόλια / Κωδικός αναφοράς | Ποσό |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Σπίτι / Supermarket  | ΑΓΟΡΑ ΜΕ ΚΑΡΤΑ  | 14/08/2022 | blah blah | -20 EUR |
| Ψυχαγωγία / Εστιατόρια  | ΑΓΟΡΑ ΜΕ ΚΑΡΤΑ  | 14/08/2022 | blah blah | -150 EUR |
