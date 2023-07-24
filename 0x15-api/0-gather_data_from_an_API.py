#!/usr/bin/python3

"""
Python script to fetch and display employee TODO list progress from the given REST API.
"""

import sys
import requests


def get_employee_todo_progress(employee_id):
    """
    Fetches and displays the employee TODO list progress.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        None
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

        # Counting completed tasks
        completed_tasks = [task["title"] for task in todos_data if task["completed"]]
        num_completed_tasks = len(completed_tasks)
        total_tasks = len(todos_data)

        # Displaying the progress
        print(f"Employee {employee_name} is done with tasks ({num_completed_tasks}/{total_tasks}):")
        for task in completed_tasks:
            print(f"\t{task}")

    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching data:", e)
        sys.exit(1)
    except (KeyError, ValueError):
        print("Error: Invalid employee ID or invalid API response")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Error: Invalid employee ID (must be an integer)")
        sys.exit(1)

