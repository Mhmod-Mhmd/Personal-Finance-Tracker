import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description


class CSV:

    CSV_FILE = "finance_data.csv"
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def entry_csv(cls, date, amount, category, description):
        entry_date = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        }

        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(entry_date)

        print('Data entries successfully!')


    @classmethod
    def csv_transaction(cls, start_date, end_date):

        df = pd.read_csv(cls.CSV_FILE)
        # print(type(df['date'][0]))
        df['date'] = pd.to_datetime(df['date'], format= cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        start_date_f = start_date.strftime(cls.FORMAT)
        end_date_f = end_date.strftime(cls.FORMAT)

        if filtered_df.empty:
            print('There is no transaction!')
        
        else:
            print(
                f'Transactions between {start_date_f} and {end_date_f}'
                )
            print(
                filtered_df.to_string(
                    index=False, formatters={'date': lambda x: x.strftime(cls.FORMAT)}
                    )
                    )
            
            total_Income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_Expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            net = total_Income - total_Expense

            print("\nSummary:")
            print(f'Total Income is: {total_Income:.2f} $')
            print(f'Total Expense is: {total_Expense:.2f} $')

            if net > 0:
                print(f'Your Net Saving is {net:.2f}')
            elif net == 0:
                print(f'There is no Saving from {start_date_f} to {end_date_f}' )

            else:
                print(f'You exceeded the spending from {start_date_f} to {end_date_f}' )

        return filtered_df




def add_data_to_csv():
    CSV.initialize_csv()

    date = get_date('Enter the date in such format "dd-mm-yyyy"',
                    default_date=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.entry_csv(date, amount, category, description)



def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add_data_to_csv()

        elif choice == '2':
            start_date = get_date('Enter the Start Date: ')
            end_date = get_date('Enter the End Date: ')
            df = CSV.csv_transaction(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)

        elif choice == '3':
            print('Exiting....')
            break

        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == '__main__':
    main()


