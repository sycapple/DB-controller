import time
from datasearch import *
from tabulate import tabulate
import random

position = None


class Cmd:
    user = None

    def __init__(self, s):
        global position
        self.s = s
        self.command = s.split(' ')[0]
        if self.command == 'ls':
            self.cmd_ls()
        elif self.command == 'cd':
            self.cmd_cd()
        elif self.command == 'generate':
            self.cmd_generate()
        elif self.command == 'search':
            self.cmd_search()
        elif self.command == 'delete':
            self.cmd_delete()
        elif self.command == 'edit':
            self.cmd_edit()
        else:
            print("wrong input")
    def cmd_ls(self):
        global position
        # Check if the position is None
        if position == None:
            # Get all the table names
            table_names = get_all_table()
            # Iterate through the table names
            for table_name in table_names:
                # Print the table name
                print(table_name)
        else:
            # Print the form of the list_all function
            self.print_form(list_all(position), position)

    def cmd_cd(self):
        global position
        # Get the table name from the command
        table_name = self.s.split(' ')[1]
        # Check if the table name is in the list of all table names
        if table_name in get_all_table():
            # Set the position to the table name
            position = table_name
            # Print the message
            print(f"get into tabel <{table_name}>")
        elif table_name == '..':
            # Set the position to None
            position = None
            # Print the message
            print(f"back to DB")
        else:
            # Print the message
            print(f'table {table_name} not found,please try again')

    def print_form(self, datas, now_position):
        # Check if the datas is not empty
        if datas:
            # Create an empty list
            values = []
            # Get the headers from the DB_Model
            headers = eval(DB_Model[now_position]).__table__.columns.keys()
            # Iterate through the datas
            for data in datas:
                # Append the data to the values list
                values.append([data.__dict__[column_name] for column_name in headers])
            # Print the table
            print(tabulate(values, headers, tablefmt="grid"))
        else:
            # Print the message
            print('No records here')

    def cmd_generate(self):
        # Get the count1 and count2 from the command
        count1 = eval(self.s.split(' ')[1])
        count2 = eval(self.s.split(' ')[2])
        # Call the user_generate function
        user_generate(count1, count2)
        # Print the message
        print(f'{count1} user added,{count2 * count1} blood pressure records added')
        # Print the form of the list_all function
        self.print_form(list_all('users')[-count1:], 'users')
        # Print the message
        print(
            '------------------------------------------------------------------------------------------------------------------------------------------')
        # Print the form of the list_all function
        self.print_form(list_all('blood_pressure')[-count1 * count2:], 'blood_pressure')

    def cmd_search(self):
        global position
        # Check if the user input is a number
        if self.s.split(' ')[1].isdigit():
            # If it is, convert it to an integer
            id = eval(self.s.split(' ')[1])
        else:
            # If not, set the username to the user input
            username = self.s.split(' ')[1]
            # Search for the user with the username
            self.user = user_search_username(username)
        # Check if the position is 'users'
        if position == 'users':
            # If it is, check if the user is found
            if not self.user:
                # If not, search for the user with the id
                self.user = user_search_id(id)
            # Print the form of the user
            self.print_form([self.user], position)
            # Initialize a flag
            flag = ''
            # Check if the flag is set
            while not flag:
                # Ask the user if they want to show all of the user's blood pressure records
                flag = input("Need to show all of the user's blood pressure records?(Y/N)")
                # If the user inputs 'Y', print the blood pressure records of the user
                if flag == 'Y':
                    self.print_form(search_user_records(self.user), 'blood_pressure')
                # If the user inputs 'N', break out of the loop
                elif flag == 'N':
                    break
                # If the user inputs something else, print an error message
                else:
                    print("Illegal input")
                    flag = ''
        else:
            # If the position is not 'users', print the form of the user's records
            self.print_form(search_user_records(self.user), position)

    def cmd_delete(self):
        global position
        if position == 'users':
            # Check if the user is inputting an id or username
            if self.s.split(' ')[1].isdigit():
                id = eval(self.s.split(' ')[1])
                self.user = user_search_id(id)
            else:
                username = self.s.split(' ')[1]
                self.user = user_search_username(username)
            # Print the user's records
            self.print_form(search_user_records(self.user), 'blood_pressure')
            # Ask the user which record to delete
            flag = input(
                f"Here are all of the <{self.user.username}>'s blood pressure records and which ones to edit(Note that this operation is not reversible)(Enter 0 to delete all records)?")
            # Delete all the records if the user inputs 0
            if flag == '0':
                print(f"The <{self.user.username}>'s all record has been deleted")
                user_delete(self.user)
                self.user = None
            # Check if the user input is a digit
            elif not flag.isdigit():
                print("Illegal input")
            # Delete the record if the user input is a digit
            else:
                print(f"The record whose id is {flag} has been deleted")
                user_delete_record(self.user, eval(flag))
                self.user.updated_at = datetime.now
        else:
            pass

    def cmd_edit(self):
        global position
        # Check if the user is in the 'users' position
        if position == 'users':
            # Check if the user is editing a specific user
            if self.s.split(' ')[1].isdigit():
                # Get the user id
                id = eval(self.s.split(' ')[1])
                # Get the user object
                self.user = user_search_id(id)
            else:
                # Get the username
                username = self.s.split(' ')[1]
                # Get the user object
                self.user = user_search_username(username)
            # Print the form
            self.print_form([self.user], position)
            # Print the blood pressure records
            self.print_form(search_user_records(self.user), 'blood_pressure')
            # Ask the user to edit the records
            flag = input(
                f"Here are all of the <{self.user.username}>'s blood pressure records and which ones to edit(Note that this operation is not reversible)(Enter 0 to edit user)?")
            # If the user is editing a specific user
            if flag == '0':
                # Ask the user to enter the parameters
                username, age, gender, height, weight = input(
                    "Enter the parameters <username>,<age>,<gender>,<height>,<weight> in the following order, separated by Spaces").split(
                    ' ')
                # Convert the parameters to integers
                age = eval(age)
                height = eval(height)
                weight = eval(weight)
                # Edit the user
                user_edit(self.user, username, age, gender, height, weight)
                # Print the new user record
                print("Here's new user record")
                # Get the new user object
                self.user = user_search_username(username)
                # Print the form
                self.print_form([self.user], position)
            # If the user is editing a specific record
            elif not flag.isdigit():
                # Print an error message
                print("Illegal input")
            # If the user is editing all records
            else:
                # Convert the flag to an integer
                flag = eval(flag)
                # Ask the user to enter the parameters
                systolic, diastolic = input(
                    "Enter the parameters <systolic>,<diastolic> in the following order, separated by Spaces").split(
                    ' ')
                # Edit the record
                blood_pressure_record_edit(self.user, flag, eval(systolic), eval(diastolic))
                # Print a success message
                print("Edit successfully!")
        else:
            # Do nothing
            pass


if __name__ == '__main__':
    print("Here is my database management terminal")
    while True:
        cmd = input(">>")
        if cmd == 'help':
            print('''
here's some cmd you can use
    1. ls                                                                               List all records/forms
    2. search <username>/<id>                                                           Query records by <username>/<id>
    3. add <username> <age> <gender> <height> <weight> <systolic> <diastolic>           Add a record named <username>
    4. delete <username>/<id>                                                           Delete a record based on the <username>
    5. edit <username>/<id>                                                             Change the target user's blood pressure/data
    6. generate <num1> <num2>                                                           Generate <num1> user records, and each user links <num2> blood pressure records
                ''')
        else:
            try:
                cmd = Cmd(cmd)
            except:
                print('Illegal input')
