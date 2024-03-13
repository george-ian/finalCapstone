# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

def reg_user():
    """
    The function reg_user registers a new user by asking for a 
    unique username and password and stores the data in the file user.txt.
    """
    
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        if new_username not in username_password:
            break
        print("User already exists! Please enter a different username!")
            
        
    while True:
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
        
            # if the passwords match, add the new username and password to the
            # dictionary and user.txt 
            print("New user registered.")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for key in username_password:
                    user_data.append(f"{key};{username_password[key]}")
                out_file.write("\n".join(user_data))
            break
        else:
            print("Passwords do not match! Please try again.") 
            
            
def update_tasks():
    """
    The function update_tasks writes task information to the file tasks.txt
    in a specific format.
    """

    with open("tasks.txt", "w") as file:

        # create a list containing data for each task
        task_list_to_write = []
        for task in task_list:
            str_attrs = [
                task["username"],
                task["title"],
                task["description"],
                task["due_date"].strftime(DATETIME_STRING_FORMAT),
                task["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task["completed"] else "No"
            ]

            # Join the task's attributes with semi-colons and add this string
            # to a new list
            task_list_to_write.append(";".join(str_attrs))

        # Write the string for each task on a separate line in the tasks.txt
        file.write("\n".join(task_list_to_write))               
            
def add_task():
    """
    Function add_task asks the user to input details of a new task, such as 
    the username of the person to whom the task will be assigned, the title,
    description, due date, and then adds the task to tasks.txt 
     
    """

    # Asks for existing username to whom this task will be assigned 
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username in username_password.keys():
            break
        print("This user does not exist. Please enter a valid username.")
            
        

    # Ask user for title and description of task
    task_title = input("Title of task: ")
    task_description = input("Description of task: ")

    # Ask user for due date and ensure it is in the correct format
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

    # Get the current date
    curr_date = date.today()

    # Add the data to the task list and to tasks.txt 
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    update_tasks()
    print("Task successfully added.")
    
def print_task(task_id, task: dict):
    """
    Function print_task takes as parameters task_id and task as dictionary, 
    then prints task's data to the console in a specific format. 
    The dictionary contains information about a specific task. Its keys are 
    "title", "username", "assigned_date", "due_date", and "description".
    
    """

    # Build a string which displays all the task information
    disp_str = f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += ("Date Assigned: \t "
                 f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += ("Due Date: \t "
                 f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
    disp_str += f"Task Description: \n {task['description']}"

    # Print this information along with corresponding task id
    print("*" * 70)
    print(f"\nTask ID: {task_id}\n" + disp_str)
    print("*" * 70)
    
def edit_task(task: dict):
    """
    The function edit_task allows the user to reassign a task to a 
    different user or edit the due date of the task.   
    
    """

    while True:
        # Request a selection from the user
        edit_choice = input("""\nSelect one of the following options:
r - Reassign task
e - Edit due date
: """).lower()

        if edit_choice == "r":
            while True:
                # Request username to whom the task will be reassigned
                # and check that it exists
                new_user = input("Enter the new username for this task: ")

                if new_user in username_password:

                    # Update dictionary for this task
                    task["username"] = new_user
                    print(f"Task reassigned to {new_user}.")
                    break

                # If username doesn't exist, print relevant message
                print("Username doesn't exist! Please try again.")
            break

        if edit_choice == "e":

            # Request new due date and ensure it is in the correct format
            while True:
                try:
                    new_date = input("New due date of task (YYYY-MM-DD): ")
                    new_date_time = \
                        datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format "
                          "specified.")

            # Update dictionary for this task
            task["due_date"] = new_date_time
            print("Due date successfully updated.")
            break

        print("Invalid input - please try again.")


def view_all():
    """
    The function view_all  prints all tasks with an identifying number 
    or a message if there are no tasks.
    """

    # Print all tasks with an identifying number
    for task_id, task in enumerate(task_list):
        print_task(task_id, task)

    # If there are no tasks, print a relevant message   
    if not task_list:
        print("There are no tasks to view!")

def view_mine():
    """
    Function view_mine allows the user to view and change the tasks 
    assigned to him.
    """

    while True:
        # Prints all the tasks that are assigned to the current user        
        my_task_ids = []
        for task_id, task in enumerate(task_list):
            if task["username"] == curr_user:
                print_task(task_id, task)
                my_task_ids.append(task_id)

        # If no tasks are assigned, print a message and exit the loop
        if not my_task_ids:
            print("You have no tasks assigned.")
            break

        # Request a selection from the user
        task_choice = input("""To select a task type the task id number.
To go back to the main menu, type '-1'.
: """)

        # If selection is one of the user's assigned tasks, provide
        # options for the user to choose
        if task_choice.isnumeric() and int(task_choice) in my_task_ids:
            print_task(task_choice, task_list[int(task_choice)])
            while True:
                user_choice = input("""Select one of the following options:
m - Mark as complete
e - Edit task
d - Select a different task
: """).lower()

                if user_choice == "m":

                    # Mark task as complete and update tasks.txt 
                    
                    task_list[int(task_choice)]["completed"] = True
                    update_tasks()
                    print("Task marked as complete.")
                    break

                if user_choice == "e" and not \
                        task_list[int(task_choice)]["completed"]:

                    # Run edit function and - when completed - update
                    # task file accordingly
                    edit_task(task_list[int(task_choice)])
                    update_tasks()
                    break

                if user_choice == "e":

                    # If task completed print relevant message and break                    
                    print("Task completed - unavailable for editing.")
                    break

                if user_choice == "d":

                    # Go back to the main menu
                    break

                print("Invalid input - please try again.\n")

        # If -1 is entered, break out of the loop to return to the main menu
        elif task_choice == "-1":
            break

        else:
            print("Invalid input - please try again.")


def generate_task_stats():
    """
    The function generate_task_stats generates statistics about a task and 
    writes them to task_overview.txt.
    """
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    # For each task, update variables accordingly
    for task in task_list:
        if task["completed"]:
            completed_tasks += 1
        elif datetime.today() > task["due_date"]:
            uncompleted_tasks += 1
            overdue_tasks += 1
        else:
            uncompleted_tasks += 1

    # Get total number of tasks
    total_tasks = len(task_list)

    # Calculate percentages for each variable and if there are no tasks, set 
    # all percentages to 0
    try:
        pc_complete = (completed_tasks / total_tasks) * 100
        pc_incomplete = (uncompleted_tasks / total_tasks) * 100
        pc_overdue = (overdue_tasks / total_tasks) * 100

    except ZeroDivisionError:
        pc_complete = pc_incomplete = pc_overdue = 0

    # write the statistics to task_overview.txt
    
    with open("task_overview.txt", "w") as file:
        file.write("Task overview\n" + "-" *20 + "\n")
        file.write(f"\nTotal number of tasks = {total_tasks}")
        file.write("\nTotal number of completed tasks = "
                          f"{completed_tasks} ({pc_complete:.1f}%)")
        file.write("\nTotal number of uncompleted tasks = "
                          f"{uncompleted_tasks} ({pc_incomplete:.1f}%)")
        file.write(f"\nTotal number of overdue tasks = {overdue_tasks} "
                          f"({pc_overdue:.1f}%)")
        
        
def generate_user_stats():
    """
    The function generate_user_stats generates statistics about the tasks 
    assigned to each user and writes this information to user_overview.txt
    """

    # Get the total number of users and tasks
    total_users = len(username_password)
    total_tasks = len(task_list)

    # Write the total number of users and tasks to user_overview.txt
    
    with open("user_overview.txt", "w") as file:
        file.write("User overview\n" + "-" *20 + "\n")
        file.write(f"\nTotal number of users = {total_users}")
        file.write(f"\nTotal number of tasks = {total_tasks}")

        # Perform calculations for each user
        for current_user in sorted(username_password):

            # Create a list of tasks assigned to the current user in the loop
            
            user_task_list = [task for task in task_list if task["username"]
                              == current_user]

            # Retrieve total number of tasks for that user
            user_total_tasks = len(user_task_list)

            # Set variables to 0
            completed_tasks = 0
            uncompleted_tasks = 0
            overdue_tasks = 0

            # For each task, update variables accordingly
            for user_task in user_task_list:
                if user_task["completed"]:
                    completed_tasks += 1
                elif datetime.today() > user_task["due_date"]:
                    uncompleted_tasks += 1
                    overdue_tasks += 1
                else:
                    uncompleted_tasks += 1

            # Calculate percentages for each variable
            try:
                pc_assigned = (user_total_tasks / total_tasks) * 100
                pc_completed = (completed_tasks / user_total_tasks) * 100
                pc_uncompleted = (uncompleted_tasks / user_total_tasks) * 100
                pc_overdue = (overdue_tasks / user_total_tasks) * 100

            # If user has no tasks assigned, set all percentages to 0
            except ZeroDivisionError:
                pc_assigned = pc_completed = pc_uncompleted = pc_overdue = 0

            # Write specific information for current user in loop to
            # .txt file
            file.write(f"\n\n> {current_user}")
            file.write("\nNumber of tasks assigned: "
                              f"{user_total_tasks} ({pc_assigned:.1f}%)")
            file.write("\nNumber of assigned tasks completed: "
                              f"{completed_tasks} ({pc_completed:.1f}%)")
            file.write("\nNumber of assigned tasks uncompleted: "
                              f"{uncompleted_tasks} ({pc_uncompleted:.1f}%)")
            file.write("\nNumber of assigned tasks overdue: "
                              f"{overdue_tasks} ({pc_overdue:.1f}%)")
            
def display_stats():
    """
    Function display_stats displays the total number of users and tasks.    
    """
    # Count number of users and tasks by counting the lines in the text files
    with open("user.txt", "r") as users:
        lines=users.readlines()
        line_counter = 0
        for line in lines:
            if line != "\n":
                line_counter += 1
                
        num_users = line_counter
    
    with open("tasks.txt", "r", encoding="utf-8") as tasks:
        lines=tasks.readlines()
        lines_counter = 0
        for line in lines:
            if line != "\n":
                lines_counter += 1
                
        num_tasks = lines_counter
    
    # Display statistics
    print("\n-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for task_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each attribute to the dictionary
    task_components = task_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login successful!")
        logged_in = True


while True:
    if curr_user=="admin":
        # presenting the menu to the admin and 
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    
        if menu == 'r':
            reg_user()
            
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()
         
        elif menu == 'vm':
            view_mine()
            
        elif menu == 'gr':
            generate_task_stats()
            generate_user_stats()
            str_to_dsp="To view the reports please open the following files: "
            str_to_dsp+="\n'task_overview.txt'\n'user_overview.txt'.\nYou can find "
            str_to_dsp+="them in the local directory."
            print(str_to_dsp)
            
        
        elif menu == 'ds': 
            display_stats()  
    
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
    
        else:
            print("You have made a wrong choice, please try again")
    else:
        # presenting the menu to all other users and 
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()
    
        if menu == 'r':
            reg_user()
            
        elif menu == 'a':
            add_task()
            
        elif menu == 'va':
            view_all()
            
    
        elif menu == 'vm':
            view_mine()
           
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
    
        else:
            print("You have made a wrong choice, please try again")
        
            
