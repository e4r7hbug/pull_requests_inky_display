#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retrieve GitHub Pull Requests assigned to logged in user."""
import json
from urllib.parse import urlparse

from invoke import run
from tabulate import tabulate


def get_user():
    """Retrieve handle of logged in user."""
    user_result = run("hub api user", hide=True)
    user_data = json.loads(user_result.stdout)

    user = user_data["login"]
    return user


def get_review_requests():
    """Retrieve Pull Requests with Review Requests.

    Returns:
        dict: json object from api.

    """
    user = get_user()

    result = run(
        f"hub api search/issues --field 'q=is:open is:pr review-requested:{user} archived:false' -X GET",
        hide=True,
    )

    data = json.loads(result.stdout)
    return data


def main():
    """Use the GitHub API to print Pull Requests with review requests."""
    data = get_review_requests()

    pull_requests = [
        {
            "url": pull_request["html_url"],
            "user": pull_request["user"]["login"],
            "title": pull_request["title"],
        }
        for pull_request in data["items"]
    ]

    table = tabulate(pull_requests, headers="keys", showindex=True)
    print(table)


if __name__ == "__main__":
    main()
