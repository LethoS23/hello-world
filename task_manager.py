# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import datetime
# We will make updates to this section later in the task so leave it for now.
# ====Login Section====
'''This section allows a user to log in.
    - Reads usernames and passwords from the user.txt file.
    - Stores them in a dictionary.
    - Uses a while loop to validate the username and password.
'''


def load_users():
    '''This code block reads the user.txt file and loads usernames and
    passwords
    into a dictionary.'''

    users = {}
    try:
        with open('user.txt', 'r') as user_file:
            for line in user_file:
                parts = line.strip().split(", ")
                if len(parts) == 2:
                    username, password = parts
                    users[username] = password
                else:
                    print(f"""Skipping invalid line in 'user.txt':
                          {line.strip()}""")
    except FileNotFoundError:
        print("""The file 'user.txt' does not exist. Please ensure it is in the
              correct directory.""")
        exit()
    return users


# ====Login Function====
'''This function handles user login. While loop to checks if the username and
    password are valid and returns the username if successful.
'''


def login(users):
    '''This code block checks if the username and password are valid.'''
    '''- Prompts for username and password.
    - Uses a while loop to validate the username and password.
    - If the username is 'exit', the program exits.
    - If the username is not 'exit', it checks if the username and password
    are valid.
    - If the username and password are valid, it returns the username.
    - If the username and password are not valid, it prompts the user to try
    again.
    '''
    while True:
        username = input("Enter your username (or type 'exit' to quit): ")
        if username.lower() == "exit":
            exit()
        password = input("Enter your password: ")
        if username in users and users[username] == password:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password. Please try again.")


# ====Main Menu====
'''This section presents the menu to the user and handles their input.'''

# ====Register User Function====
'''This function allows the admin to register a new user.'''


def register_user():
    '''Allows the admin to register a new user.
    - Checks if current user is admin
    - Prompts for a new username and password.
    - Confirms the password before saving it to the user.txt file.
    - Appends the new user to the file without overwriting existing data.
    '''
    # Load existing users to check if admin exists
    users = load_users()
    if "admin" not in users:
        print("Error: Admin user does not exist.")
        return

    # Check if current user is admin
    username = input("Please enter your username to verify admin status: ")
    password = input("Enter your password: ")

    if username != "admin" or users["admin"] != password:
        print("Only admin can register new users.")
        return

    new_username = input("Enter a new username: ")
    new_password = input("Enter a new password: ")
    confirm_password = input("Confirm the new password: ")

    if new_password == confirm_password:
        try:
            with open('user.txt', 'a') as user_file:
                # Ensures that the new user starts on a new line
                user_file.write(f"\n{new_username}, {new_password}")
            print("New user registered successfully!")
        except FileNotFoundError:
            print("""The file 'user.txt' does not exist. Please ensure it is in
                  the correct directory.""")
    else:
        print("Passwords do not match. Please try again.")


# ====Add Task Function====
'''This function allows a user to add a new task. It prompts for task details
    and appends them to the task.txt file.'''


def add_task():
    '''This code block allows a user to add a new task.
    - Prompts for the username of the person the task is assigned to,
    - the title of the task,
    - the description of the task, and
    - the due date of the task.
    - Gets the current date.
    - Appends the data to the task.txt file.
    - Includes 'No' to indicate that the task is not complete.
    '''
    # Load users to validate username
    users = load_users()
    while True:
        task_username = input(
            "Enter the username of the person the task is assigned to: "
        )
        if task_username in users:
            break
        print("User does not exist. Please enter a valid username.")

    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")

    while True:
        task_due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
        try:
            datetime.strptime(task_due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")

    current_date = datetime.now().strftime("%Y-%m-%d")
    task_completed = "No"
    try:
        with open('tasks.txt', 'a') as task_file:
            # Write task details in a single line, separated by commas
            task_file.write(
                f"{task_username}, {task_title}, {task_description}, "
                f"{current_date}, {task_due_date}, {task_completed}\n"
            )
        print("Task added successfully!")
    except FileNotFoundError:
        print("""The file 'tasks.txt' does not exist. Please ensure it is in
              the correct directory.""")


# ====View All Tasks Function====
'''This function reads and prints all tasks from task.txt. It handles
    file not found errors.'''


def read_tasks():
    try:
        with open('tasks.txt', 'r') as task_file:
            tasks = []
            for line in task_file:
                task_data = line.strip().split(", ")
                if len(task_data) == 6:
                    tasks.append(task_data)
            return tasks
    except FileNotFoundError:
        print("The file 'tasks.txt' does not exist. Please ensure it is in "
              "the correct directory.")
        return []


def view_all_tasks():
    '''This code block reads the task.txt file and prints all tasks.
    - Reads each line from the file.
    - Splits the line where there is a comma and space.
    - Prints the results in a formatted way.
    - Uses a for loop to read the file line by line.
    '''
    try:
        with open('tasks.txt', 'r') as task_file:
            tasks = task_file.readlines()

            if not tasks:
                print("\nNo tasks found.")
                return

            print("\nAll Tasks:")
            for i, line in enumerate(tasks, 1):
                task_data = line.strip().split(", ")
                if len(task_data) == 6:
                    print(f"\nTask {i}:")
                    print("-" * 50)
                    print(f"Task Assigned To: {task_data[0]}")
                    print(f"Task Title: {task_data[1]}")
                    print(f"Task Description: {task_data[2]}")
                    print(f"Date Assigned: {task_data[3]}")
                    print(f"Due Date: {task_data[4]}")
                    print(f"Task Completed: {task_data[5]}")
                    print("-" * 50)

    except FileNotFoundError:
        print("The file 'tasks.txt' does not exist. Please ensure it is in the"
              "correct directory.")


# ====View My Tasks Function====
'''This function allows a user to view their assigned tasks. It filters tasks
    based on the logged-in user's username.'''


def view_my_tasks(username):
    '''This code block reads the task.txt file and prints tasks assigned to
    the logged-in user.
    - Reads each line from the file.
    - Splits the line where there is a comma and space.
    - Checks if the username of the logged-in user matches the username in
    the file.
    - If they match, prints the task in a formatted way with task numbers.
    '''
    try:
        with open('tasks.txt', 'r') as task_file:
            tasks = task_file.readlines()
            user_tasks = []

            # Get all tasks for the user
            for task in tasks:
                task_data = task.strip().split(", ")
                if task_data[0] == username and len(task_data) == 6:
                    user_tasks.append(task_data)

            if not user_tasks:
                print(f"\nNo tasks assigned to {username}")
                return

            print(f"\nTasks assigned to {username}:")
            for i, task in enumerate(user_tasks, 1):
                print(f"\nTask {i}:")
                print("-" * 50)
                print(f"Task Title: {task[1]}")
                print(f"Task Description: {task[2]}")
                print(f"Date Assigned: {task[3]}")
                print(f"Due Date: {task[4]}")
                print(f"Task Completed: {task[5]}")
                print("-" * 50)

    except FileNotFoundError:
        print("The file 'tasks.txt' does not exist. Please ensure it is in the"
              "correct directory.")


def display_statistics():
    '''This function displays statistics about total tasks and users.
    Only accessible by admin users.
    '''
    try:
        # Count total users
        with open('user.txt', 'r') as user_file:
            user_count = sum(1 for line in user_file if line.strip())

        # Count total tasks
        with open('tasks.txt', 'r') as task_file:
            task_count = sum(1 for line in task_file if line.strip())

        print("\n===== Statistics =====")
        print("-" * 20)
        print(f"Total Users: {user_count}")
        print(f"Total Tasks: {task_count}")
        print("-" * 20)

    except FileNotFoundError:
        print("Error: Required files not found. Please ensure both 'user.txt'"
              "and 'tasks.txt' exist.")


# ====Main Program====
'''This section runs the main program.'''


def main():
    '''This code block runs the main program.
    - Loads users from the user.txt file.
    - Prompts for login.
    - Displays the menu and handles user input.
    - Calls the appropriate functions based on user input.
    '''
    users = load_users()
    username = login(users)

    while True:
        # Display of different menu option for admin only
        if username == "admin":
            menu = input('''\nSelect one of the following options:\n
r - register a user
a - add task
va - view all tasks
vm - view my tasks
s - display statistics
e - exit
: ''').lower()
        else:
            menu = input('''\nSelect one of the following options:\n
r - register a user
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower()

        if menu == 'r' and username == 'admin':
            register_user()
        elif menu == 'r':
            print("Only the admin user can register new users.")
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all_tasks()
        elif menu == 'vm':
            view_my_tasks(username)
        elif menu == 's' and username == 'admin':
            display_statistics()
        elif menu == 'e':
            print("Goodbye!!!")
            exit()
        else:
            print("You have entered an invalid input. Please try again.")


# ====End of Code====
# ====Main Program Execution====
''' This code block runs the main program.'''
if __name__ == "__main__":
    main()
