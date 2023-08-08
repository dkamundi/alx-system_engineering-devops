#!/usr/bin/python3

"""
Recursive function to query the Reddit API, parse hot article titles, and print a sorted count of keywords.
"""

import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """
    Recursively queries the Reddit API, parses hot article titles, and prints a sorted count of keywords.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count occurrences for.
        after (str, optional): Pagination parameter for Reddit API. Defaults to None.
        word_count (dict, optional): Dictionary to store keyword counts. Defaults to an empty dictionary.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Custom User Agent"}  # Set a custom User-Agent
    params = {"after": after} if after else None

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        try:
            data = response.json()
            posts = data["data"]["children"]

            for post in posts:
                title = post["data"]["title"].lower() # Convert title to lowercase

                for keyword in word_list:
                    if keyword in title:
                        # Count keyword occurrences
                        word_count[keyword] = word_count.get(keyword, 0) + title.count(keyword)

            after = data["data"]["after"]

            if after:
                return count_words(subreddit, word_list, after, word_count)
            else:
                sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
                for keyword, count in sorted_counts:
                    print(f"{keyword}: {count}")
        except (KeyError, ValueError):
            return
    else:
        return

