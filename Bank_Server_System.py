import csv
import random
import re
import os
from datetime import datetime

# -------- PATH CONFIG --------

config_file = "config.txt"

if os.path.exists(config_file):
    with open(config_file, "r") as f:
        folder_path = f.read().strip()
    print("Using saved path:", folder_path)
else:
    folder_path = input("Enter folder path to save CSV files: ")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(config_file, "w") as f:
        f.write(folder_path)

    print("Path saved for future use:", folder_path)

# Ensure folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

accounts_file = os.path.join(folder_path, "accounts.csv")
login_file = os.path.join(folder_path, "login.csv")


# -------- CREATE FILES WITH HEADERS --------

def create_files_with_headers():

    if not os.path.exists(accounts_file):
        with open(accounts_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Account Number",
                "Account Holder Name",
                "DOB",
                "Age",
                "Gender",
                "Phone Number",
                "Email",
                "ID Type",
                "ID Number",
                "Balance"
            ])

    if not os.path.exists(login_file):
        with open(login_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Username",
                "Password",
                "Account Number"
            ])


create_files_with_headers()


# -------- ACCOUNT NUMBER --------

def generate_account_number():
    return str(random.randint(100000000000, 999999999999))


# -------- VALIDATIONS --------

def get_phone():
    while True:
        phone = input("Enter Phone Number (10 digits): ")
        if phone.isdigit() and len(phone) == 10:
            return phone
        print("Invalid phone number")


def get_email():
    while True:
        email = input("Enter Gmail ID: ")
        if email.endswith("@gmail.com"):
            return email
        print("Email must end with @gmail.com")


def get_dob():
    while True:
        dob = input("Enter DOB (DD-MM-YYYY): ")
        try:
            birth = datetime.strptime(dob, "%d-%m-%Y")
            today = datetime.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return dob, age
        except:
            print("Invalid date format")


def get_gender():
    while True:
        print("1 Male")
        print("2 Female")
        print("3 Transgender")

        g = input("Choose Gender: ")

        if g == "1":
            return "Male"
        elif g == "2":
            return "Female"
        elif g == "3":
            return "Transgender"
        else:
            print("Invalid option")


def get_identity():
    while True:
        print("1 Aadhaar")
        print("2 PAN")

        ch = input("Choose ID Proof: ")

        if ch == "1":
            num = input("Enter Aadhaar Number: ")
            if num.isdigit() and len(num) == 12:
                return "Aadhaar", num
            print("Aadhaar must be 12 digits")

        elif ch == "2":
            num = input("Enter PAN Number: ").upper()
            if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', num):
                return "PAN", num
            print("Invalid PAN format")


def get_ifsc():
    while True:
        code = input("Enter IFSC Code: ").upper()
        if re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', code):
            return code
        print("Invalid IFSC format")


def get_account_number():
    while True:
        acc = input("Receiver Account Number: ")
        if acc.isdigit() and len(acc) == 12:
            return acc
        print("Account number must be 12 digits")


# -------- USERNAME --------

def get_username():
    while True:
        username = input("Create Username: ")

        try:
            with open(login_file) as f:
                reader = csv.reader(f)
                next(reader)  # skip header

                for row in reader:
                    if row[0] == username:
                        print("Username already exists")
                        break
                else:
                    return username
        except:
            return username


# -------- CREATE ACCOUNT --------

def create_account():

    name = input("Enter Name: ")
    dob, age = get_dob()
    gender = get_gender()
    phone = get_phone()
    email = get_email()
    id_type, id_num = get_identity()
    username = get_username()
    password = input("Create Password: ")
    balance = float(input("Enter Initial Deposit: "))

    acc_no = generate_account_number()

    with open(accounts_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([acc_no, name, dob, age, gender, phone, email, id_type, id_num, balance])

    with open(login_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, password, acc_no])

    print("Account Created Successfully")
    print("Your Account Number:", acc_no)


# -------- LOGIN --------

def login():

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        with open(login_file) as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                if row[0] == username and row[1] == password:
                    print("Login Successful")
                    return row[2], password
    except:
        pass

    print("Invalid login")
    return None, None


# -------- CHECK BALANCE --------

def check_balance(acc, password):

    verify = input("Enter password to view balance: ")

    if verify != password:
        print("Incorrect password")
        return

    with open(accounts_file) as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if row[0] == acc:
                print("Current Balance:", row[9])
                return


# -------- DEPOSIT --------

def deposit_money(acc, password):

    amount = float(input("Enter amount to deposit: "))

    verify = input("Enter login password to confirm: ")

    if verify != password:
        print("Incorrect password")
        return

    accounts = []

    with open(accounts_file) as f:
        reader = csv.reader(f)
        accounts = list(reader)

    for row in accounts[1:]:
        if row[0] == acc:
            row[9] = str(float(row[9]) + amount)
            print("Deposit Successful")
            print("Updated Balance:", row[9])

    with open(accounts_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(accounts)


# -------- NET BANKING --------

def net_banking_menu(acc, password):

    while True:

        print("\n----- NET BANKING -----")
        print("1 Transfer Money")
        print("2 Check Balance")
        print("3 Back")

        ch = input("Choose option: ")

        if ch == "1":

            receiver = get_account_number()
            ifsc = get_ifsc()
            amount = float(input("Enter Amount: "))

            verify = input("Enter password to confirm transfer: ")

            if verify != password:
                print("Incorrect password")
                continue

            accounts = []

            with open(accounts_file) as f:
                accounts = list(csv.reader(f))

            sender_balance = 0

            for row in accounts[1:]:
                if row[0] == acc:
                    sender_balance = float(row[9])

            if sender_balance < amount:
                print("Insufficient balance")
                continue

            receiver_found = False

            for row in accounts[1:]:
                if row[0] == acc:
                    row[9] = str(float(row[9]) - amount)

                if row[0] == receiver:
                    row[9] = str(float(row[9]) + amount)
                    receiver_found = True

            if not receiver_found:
                print("Receiver account not found")
                continue

            with open(accounts_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(accounts)

            print("Transfer Successful")

        elif ch == "2":
            check_balance(acc, password)

        elif ch == "3":
            break


# -------- MONEY TRANSFER --------

def money_transfer_menu(acc, password):

    while True:

        print("\n----- MONEY TRANSFER -----")
        print("1 Net Banking")
        print("2 UPI")
        print("3 Wallet")
        print("4 Back")

        ch = input("Choose option: ")

        if ch == "1":
            net_banking_menu(acc, password)

        elif ch == "2":
            print("UPI Feature Coming Soon")

        elif ch == "3":
            print("Wallet Feature Coming Soon")

        elif ch == "4":
            break


# -------- DASHBOARD --------

def dashboard(acc, password):

    while True:

        print("\n----- USER DASHBOARD -----")
        print("1 Money Transfer")
        print("2 Deposit Money")
        print("3 Logout")

        ch = input("Choose option: ")

        if ch == "1":
            money_transfer_menu(acc, password)

        elif ch == "2":
            deposit_money(acc, password)

        elif ch == "3":
            print("Logged Out")
            break


# -------- MAIN --------

while True:

    print("\n------ QUICK BANK ------")
    print("1 Create Account")
    print("2 Login")
    print("3 Exit")

    choice = input("Choose option: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        acc, password = login()
        if acc:
            dashboard(acc, password)

    elif choice == "3":
        print("Thank You For Using Quick Bank")
        break

    else:
        print("Invalid option")