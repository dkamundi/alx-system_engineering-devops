#!/usr/bin/python3

"""
Recursive function to query the Reddit API and return a list of titles for all hot articles in a given subreddit.
"""

import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and appends titles of hot articles to the list.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list, optional): The list to store hot article titles. Defaults to an empty list.
        after (str, optional): Pagination parameter for Reddit API. Defaults to None.

    Returns:
        list: List of titles for all hot articles, or None if no results are found.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Custom Uer Agent"} # Set a custom User-Agent
    params = {"after": after} if after else None

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        try:
            data = response.json()
            posts = data["data"]["children"]

            if not posts:
                return None

            for post in posts:
                title = post["data"]["title"]
                hot_list.append(title)

            after = data["data"]["after"]

            if after:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        except (KeyError, ValueError):
            return None
    else:
        return None

