import gspread
from google.oauth2.service_account import Credentials

import datetime


ascii_art_header = r"""


|_   _|__ _  ___ | | __|  \/  |  __ _  ___ | |_  ___  _ __
   | | / _` |/ __|| |/ /| |\/| | / _` |/ __|| __|/ _ \| '__|
   | || (_| |\__ \|   < | |  | || (_| |\__ \| |_|  __/| |
   |_| \__,_||___/|_|\_\|_|  |_| \__,_||___/ \__|\___||_|


"""

def get_google_sheets_client():
    creds = Credentials.from_service_account_file('creds.json')
    return gspread.authorize(creds)


def load_tasks():
    global tasks

    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []


def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


def add_task(title, description, status='Pending'):
    deadline = input("Enter task deadline (YYYY-MM-DD) or leave empty: ")
    if deadline == "":
        deadline = None
    else:
        try:
            datetime.datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("Invalid deadline format. Please enter in YYYY-MM-DD.")
            return

    new_task = {
        'title': title,
        'description': description,
        'status': status,
        "deadline": deadline
    }

    tasks.append(new_task)
    save_tasks()
    print("Tasks added successfully.")


def update_task(index, title=None, description=None, status=None):
    if index < 0 or index >= len(tasks):
        print("Invalid task index.")
        return

    task = tasks[index]
    if title is not None:
        task['title'] = title
    if description is not None:
        task['description'] = description
    if status is not None:
        task['status'] = status

    save_tasks()
    print("Task updated successfully.")


def list_tasks():
    print("List of Tasks:")
    for i, task in enumerate(tasks):
        deadline = task.get('deadline')
        formatted_deadline = (
            datetime.datetime.strptime(deadline, "%Y-%m-%d")
            .strftime("%Y-%m-%d")
        )

        if deadline:
            print(f"{i + 1}. Title: {task['title']}, "
                  f"Description: {task['description']}, "
                  f"Status: {task['status']}, "
                  f"Deadline: {formatted_deadline}")
        else:
            print(f"{i + 1}. Title: {task['title']}, "
                  f"Description: {task['description']}, "
                  f"Status: {task['status']}, "
                  "Deadline: None")


def delete_task(index):
    if index < 0 or index >= len(tasks):
        print("Invalid task index.")
        return

    del tasks[index]
    save_tasks()
    print("Task deleted successfully.")


def filter_tasks():
    print("\nTask Filtering")
    print("1. Filter by Priority")
    print("2. Filter by Due Date")
    print("3. Filter by Status")
    choice = input("Enter your choice: ")

    filtered_tasks = tasks

    if choice == "1":
        priority = input("Enter priority level (High, Medium, Low): ")
        filter_by_priority(tasks, priority)
    elif choice == "2":
        filter_by_due_date(filtered_tasks)
    elif choice == "3":
        filter_by_status(filtered_tasks)
    else:
        print("Invalid choice. Please enter a valid option.")


def filter_by_priority(tasks, priority):
    filtered_tasks = [
        task for task in tasks if task.get('priority') == priority
    ]
    if not filtered_tasks:
        print(f"No tasks matching the specified priority level ({priority}).")
    else:
        print("Filtered Tasks:")
        for i, task in enumerate(filtered_tasks):
            print(
                f"{i + 1}. Title: {task['title']}, "
                f"Priority: {task['priority']}"
            )


def filter_by_due_date(filtered_tasks):
    due_date = input("Enter the due date (YYYY-MM-DD): ")
    filtered_tasks = [
        task for task in filtered_tasks if task.get("deadline") == due_date
    ]
    if not filtered_tasks:
        print("No tasks matching the specified due date.")
    else:
        print("Filtered Tasks:")
        for i, task in enumerate(filtered_tasks):
            print(
                f"{i + 1}. Title: {task['title']}, "
                f"Due Date: {task['deadline']}"
            )


def filter_by_status(filtered_tasks):
    status = input("Enter the status (e.g., Pending, In Completed): ")
    filtered_tasks = [
        task for task in filtered_tasks if task.get('status') == status
        ]

    if not filtered_tasks:
        print("No tasks matching the specified status.")
    else:
        print("Filtered Tasks:")
        for i, task in enumerate(filtered_tasks):
            print(f"{i + 1}. Title: {task['title']}, Status: {task['status']}")


def sort_tasks():
    global tasks
    tasks.sort(key=lambda x: x.get('deadline', ''))

    print("\nTask sorted by due date.")
    list_tasks()


def sort_tasks_by_priority():
    global tasks
    tasks.sort(key=lambda x: x.get('priority', ''))

    print("\nTask sorted by priority.")
    list_tasks()


def sort_tasks_by_status():
    global tasks
    tasks.sort(key=lambda x: x.get('status', ''))

    print("\nTask sorted by status.")
    list_tasks()


def task_master():
    print(ascii_art_header)
    load_tasks()

    while True:
        print("\nTaskMaster - Task Management App!")
        print("1. Add Task")
        print("2. Update Task")
        print("3. List Tasks")
        print("4. Delete Task")
        print("5. Filter Tasks")
        print("6. Sort Tasks")
        print("7. Exit")

        choice = int(input("Enter your choice: "))

        try:
            choice = int(choice)
            if choice < 1 or choice > 7:
                raise ValueError("Invalid choice.")
        except ValueError as e:
            print(f"Error: {e}")
            print("Please enter a valid integer between 1 and 7.")
            continue

        if choice == 1:
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(title, description)
        elif choice == 2:
            list_tasks()
            index = int(input("Enter the index of the task to update: ")) - 1
            print("1. Update Title")
            print("2. Update Description")
            print("3. Update Status")
            update_choice = input("Enter your choice: ")

            if update_choice == "1":
                title = input("Enter new title: ")
                update_task(index, title=title)
            elif update_choice == "2":
                description = input("Enter new description: ")
                update_task(index, description=description)
            elif update_choice == "3":
                status = input("Enter new status: ")
                update_task(index, status=status)
            else:
                print("Invalid choice. Please enter a valid option.")

        elif choice == 3:
            list_tasks()
        elif choice == 4:
            list_tasks()
            index = int(input("Enter the index of the task to delete: ")) - 1
            delete_task(index)
        elif choice == 5:
            filter_tasks()
        elif choice == 6:
            print("1. Sort by Due Date")
            print("2. Sort by Priority")
            print("3. Sort by Status")
            sort_choice = input("Enter your choice: ")

            if sort_choice == "1":
                sort_tasks()
            elif sort_choice == "2":
                sort_tasks_by_priority()
            elif sort_choice == "3":
                sort_tasks_by_status()
            else:
                print("Invalid choice. Please enter a valid option.")
        elif choice == 7:
            print("Exiting TaskMaster. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":

    task_master()
