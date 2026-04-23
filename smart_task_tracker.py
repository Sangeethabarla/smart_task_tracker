import json
import os
from datetime import datetime

FILE_NAME = 'tasks.json'
PRIORITIES = {'high', 'medium', 'low'}
PRIORITY_WEIGHT = {'high': 3, 'medium': 2, 'low': 1}

def print_separator(char='-', length=60):
    """Utility to print a separator line for cleaner CLI output."""
    print(char * length)

def load_tasks():
    """Loads tasks from a JSON file. Returns an empty list if not found."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not load tasks (file may be corrupted). Starting clean.")
        return []

def save_tasks(tasks):
    """Saves all tasks into the JSON file."""
    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4)
    except IOError:
        print("Error: Could not save tasks to file.")

def validate_date(date_text):
    """Checks if the provided date string is in YYYY-MM-DD format."""
    if not date_text:
        return True
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_overdue(date_text, completed):
    """Returns True if the task is pending and past its due date."""
    if not date_text or completed:
        return False
    try:
        due_date = datetime.strptime(date_text, '%Y-%m-%d').date()
        return due_date < datetime.now().date()
    except ValueError:
        return False

def format_task_display(index, task):
    """Returns a formatted string representing a single task."""
    status = "Completed" if task.get('completed') else "Pending"
    priority = task.get('priority', 'low').capitalize()
    
    # Highlight high priority tasks (!!!)
    if priority == 'High':
        priority = f"!!! {priority} !!!"
        
    date_info = task.get('due_date') if task.get('due_date') else 'No Due Date'
    
    # Show overdue status if applicable
    if is_overdue(task.get('due_date'), task.get('completed')):
        date_info += " (OVERDUE)"
        
    return f"[{index}] {task['name']} | Priority: {priority} | Status: {status} | Due: {date_info}"

def add_task(tasks):
    """Prompts user and adds a new task to the list."""
    print("\n--- ADD NEW TASK ---")
    name = input("Enter task name: ").strip()
    if not name:
        print("Error: Task name cannot be empty.")
        return

    priority = input("Enter priority (High/Medium/Low) [Default: Low]: ").strip().lower()
    if not priority:
        priority = 'low'
    elif priority not in PRIORITIES:
        print("Invalid priority. Setting to 'Low'.")
        priority = 'low'

    due_date = input("Enter due date (YYYY-MM-DD) or leave empty: ").strip()
    if due_date and not validate_date(due_date):
        print("Error: Invalid date format. Task not added.")
        return

    task = {
        'name': name,
        'priority': priority,
        'completed': False,
        'due_date': due_date if due_date else None,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    tasks.append(task)
    print("Success: Task added successfully!")

def view_tasks(tasks, display_list=None):
    """Displays tasks. Separates pending and completed with total count."""
    # display_list expects a list of tuples: (original_index, task)
    if display_list is None:
        display_list = list(enumerate(tasks))
        
    print("\n=== TASK LIST ===")
    if not display_list:
        print("No tasks found.")
        return

    pending_tasks = [(i, t) for i, t in display_list if not t['completed']]
    completed_tasks = [(i, t) for i, t in display_list if t['completed']]

    print_separator('=')
    print(f"Total Tasks: {len(display_list)} (Pending: {len(pending_tasks)}, Completed: {len(completed_tasks)})")
    
    if pending_tasks:
        print_separator('-')
        print("PENDING TASKS:")
        for idx, t in pending_tasks:
            # Display index is 1-based (idx + 1)
            print(format_task_display(idx + 1, t))

    if completed_tasks:
        print_separator('-')
        print("COMPLETED TASKS:")
        for idx, t in completed_tasks:
            print(format_task_display(idx + 1, t))
    print_separator('=')

def get_task_index(tasks, action_name):
    """Helper method to safely prompt user for a valid task index."""
    if not tasks:
        print("No tasks available to modify.")
        return None
        
    try:
        idx_str = input(f"Enter the index of the task to {action_name}: ").strip()
        idx = int(idx_str)
        if 1 <= idx <= len(tasks):
            return idx - 1
        else:
            print("Error: Task index out of range.")
            return None
    except ValueError:
        print("Error: Please enter a valid number.")
        return None

def mark_complete(tasks):
    """Marks a pending task as completed."""
    print("\n--- MARK TASK AS COMPLETED ---")
    idx = get_task_index(tasks, "mark complete")
    if idx is not None:
        if tasks[idx]['completed']:
            print("Notice: Task is already marked as completed.")
        else:
            tasks[idx]['completed'] = True
            print(f"Success: Task '{tasks[idx]['name']}' marked as completed.")

def delete_task(tasks):
    """Deletes a task from the list after prompting for confirmation."""
    print("\n--- DELETE TASK ---")
    idx = get_task_index(tasks, "delete")
    if idx is not None:
        task_name = tasks[idx]['name']
        confirm = input(f"Are you sure you want to delete '{task_name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            removed = tasks.pop(idx)
            print(f"Success: Task '{removed['name']}' has been deleted.")
        else:
            print("Deletion cancelled.")

def search_tasks(tasks):
    """Searches tasks by a keyword in their name (case-insensitive)."""
    print("\n--- SEARCH TASKS ---")
    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        print("Error: Keyword cannot be empty.")
        return
        
    results = [(i, t) for i, t in enumerate(tasks) if keyword in t['name'].lower()]
    if results:
        print(f"\nSearch results for '{keyword}':")
        view_tasks(tasks, results)
    else:
        print(f"No tasks found containing '{keyword}'.")

def filter_tasks(tasks):
    """Filters tasks based on selected criteria (Priority or Status)."""
    print("\n--- FILTER TASKS ---")
    print("1. Filter by Priority")
    print("2. Filter by Status (Completed/Pending)")
    choice = input("Select an option (1-2): ").strip()
    
    results = []
    if choice == '1':
        priority = input("Enter priority (High/Medium/Low): ").strip().lower()
        results = [(i, t) for i, t in enumerate(tasks) if t['priority'] == priority]
    elif choice == '2':
        status = input("Enter status (C for Completed, P for Pending): ").strip().lower()
        if status == 'c':
            results = [(i, t) for i, t in enumerate(tasks) if t['completed']]
        elif status == 'p':
            results = [(i, t) for i, t in enumerate(tasks) if not t['completed']]
        else:
            print("Error: Invalid status input.")
            return
    else:
        print("Error: Invalid choice.")
        return
        
    if results:
        view_tasks(tasks, results)
    else:
        print("No tasks matched your filter criteria.")

def sort_tasks(tasks):
    """Sorts tasks systematically either by priority or by due date."""
    print("\n--- SORT TASKS ---")
    print("1. Sort by Priority (High > Medium > Low)")
    print("2. Sort by Due Date")
    choice = input("Select an option (1-2): ").strip()
    
    if choice == '1':
        tasks.sort(key=lambda t: PRIORITY_WEIGHT.get(t['priority'], 1), reverse=True)
        print("Success: Tasks sorted by priority.")
    elif choice == '2':
        # Default faraway date for tasks with no due_date to put them at the bottom
        def get_date(t):
            return t['due_date'] if t['due_date'] else "9999-99-99"
        tasks.sort(key=get_date)
        print("Success: Tasks sorted by due date.")
    else:
        print("Error: Invalid choice.")
        return
        
    view_tasks(tasks)

def main_menu():
    """Main application loop containing the interactive menu interface."""
    tasks = load_tasks()
    
    while True:
        print("\n" + "="*60)
        print("             SMART TASK & PRODUCTIVITY TRACKER")
        print("="*60)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Filter Tasks")
        print("7. Sort Tasks")
        print("8. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            search_tasks(tasks)
        elif choice == '6':
            filter_tasks(tasks)
        elif choice == '7':
            sort_tasks(tasks)
        elif choice == '8':
            print("\nSaving tasks...")
            save_tasks(tasks)
            print("Goodbye! Have a productive day!")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main_menu()
