#!/usr/bin/python3

"""
Python script to fetch employee TODO list progress from the given REST API
and export it to JSON and CSV formats.
"""

import sys
import requests
import csv
import json


def get_employee_todo_progress(employee_id):
    """
    Fetches the employee TODO list progress.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        (str, list): A tuple containing the employee name and a list of completed tasks.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    employee_url = f"{base_url}/users/{employee_id}"
    todos_url = f"{base_url}/todos?userId={employee_id}"

    try:
        # Fetching employee information
        employee_response = requests.get(employee_url)
        employee_data = employee_response.json()

        # Check if employee exists
        if "name" not in employee_data:
            print(f"Error: Employee with ID {employee_id} not found.")
            sys.exit(1)

        employee_name = employee_data["name"]

        # Fetching TODO list for the employee
        todos_response = requests.get(todos_url)
        todos_data = todos_response.json()

        # Extracting completed tasks
        completed_tasks = [
            {"task": task["title"], "completed": task["completed"], "username": employee_name}
            for task in todos_data if task["completed"]
        ]

        return employee_name, completed_tasks

    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching data:", e)
        sys.exit(1)
    except (KeyError, ValueError):
        print("Error: Invalid employee ID or invalid API response")
        sys.exit(1)


def export_to_csv(employee_id, employee_name, completed_tasks):
    """
    Exports the employee TODO list progress to a CSV file.

    Args:
        employee_id (int): The ID of the employee.
        employee_name (str): The name of the employee.
        completed_tasks (list): List of completed tasks.

    Returns:
        None
    """
    filename = f"{employee_id}.csv"
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in completed_tasks:
            csv_writer.writerow([employee_id, employee_name, "true", task["task"]])

    print(f"Data exported to {filename}")


def export_to_json(employee_id, completed_tasks):
    """
    Exports the employee TODO list progress to a JSON file.

    Args:
        employee_id (int): The ID of the employee.
        completed_tasks (list): List of completed tasks.

    Returns:
        None
    """
    data = {str(employee_id): completed_tasks}
    filename = f"{employee_id}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f"Data exported to {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gather_data_and_export_to_JSON.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        employee_name, completed_tasks = get_employee_todo_progress(employee_id)
        print(f"Employee {employee_name} is done with tasks ({len(completed_tasks)}/{employee_id}):")
        for task in completed_tasks:
            print(f"\t{task['task']}")

        export_to_csv(employee_id, employee_name, completed_tasks)
        export_to_json(employee_id, completed_tasks)

    except ValueError:
        print("Error: Invalid employee ID (must be an integer)")
        sys.exit(1)

