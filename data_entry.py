from datetime import datetime

CATETORIES = {'I': 'Income', 'E': 'Expense'}
FORMAT = "%d-%m-%Y"

def get_date(prompt, default_date = False):

    date_entry = input(prompt)

    if default_date and not date_entry:
        return datetime.today().strftime(FORMAT)
    
    try:
        vaild_date = datetime.strptime(date_entry, FORMAT)
        return vaild_date.strftime(FORMAT)
    except ValueError:
        print('Please enter the date in such format "dd-mm-yyyy"')
        return get_date(prompt, default_date)
    

def get_amount():

    try:
        amount = float(input("Enter the Amount by $: "))
        if amount <= 0:
            print("Amount Can't be Negative or Zero")
            return get_amount()
        
        return amount

    except ValueError:
        print("Amount Can't be empty Pless Enter a Value")
        return get_amount()
    

def get_category():
    catetory = input("Enter a label 'I' for Income and 'E' for Expense: ").upper()

    if catetory in CATETORIES:
        return CATETORIES[catetory]
    
    print('Invaild category label, Please Enter the right Label ( I or E )')
    return get_category()

    

def get_description(default = 'Saving'):

    desc = input('Enter the description (Optional): ').title()

    if desc:
        return desc
    return default

