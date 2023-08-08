#!/usr/bin/python3

"""
Queries the Reddit API and returns the number of subscribers for a given subreddit.
"""

import requests

def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "Customer User Agent"} # Set a custom User-Agent

    response = requests.get(url, headers=headers, allow_redirects=False)


    if response.status_code == 200:
        try:
            data = response.json()
            subscribers = data["data"]["subscribers"]
            return subscribers
        except (KeyError, ValueError):
            return 0
    else:
        return 0

