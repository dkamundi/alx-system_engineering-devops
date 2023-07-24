#!/usr/bin/python3

"""
Python script to fetch employee TODO list progress from the given REST API
and export it to a JSON file.
"""

import sys
import requests
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
            {
                "username": employee_name,
                "task": task["title"],
                "completed": task["completed"]
            }
            for task in todos_data
        ]

        return completed_tasks

    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching data:", e)
        sys.exit(1)
    except (KeyError, ValueError):
        print("Error: Invalid employee ID or invalid API response")
        sys.exit(1)


def export_to_json(todo_data):
    """
    Exports the employee TODO list progress to a JSON file.

    Args:
        todo_data (dict): Dictionary containing employee ID as key and the list of completed tasks.

    Returns:
        None
    """
    filename = "todo_all_employees.json"
    with open(filename, 'w') as json_file:
        json.dump(todo_data, json_file, indent=4)

    print(f"Data exported to {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: python3 gather_data_and_export_to_JSON.py")
        sys.exit(1)

    try:
        # Fetching TODO list for all employees and organizing the data by employee ID
        todo_data = {}
        for employee_id in range(1, 11):  # Assuming employee IDs are from 1 to 10
            completed_tasks = get_employee_todo_progress(employee_id)
            todo_data[str(employee_id)] = completed_tasks

        export_to_json(todo_data)

    except ValueError:
        print("Error: Invalid employee ID (must be an integer)")
        sys.exit(1)

