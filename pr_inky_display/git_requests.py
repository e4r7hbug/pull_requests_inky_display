#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retrieve GitHub Pull Requests assigned to logged in user."""
import json
import os
import pathlib
from urllib.parse import urlparse

import requests
import yaml
from invoke import run
from tabulate import tabulate

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

HUB_YML = os.getenv("HUB_YML", "~/.config/hub")
HUB_CONFIG_FILE = pathlib.Path(HUB_YML).expanduser()

GH_HOSTS_YML = os.getenv("GH_HOSTS_YML", "~/.config/gh/hosts.yml")
GH_CONFIG_FILE = pathlib.Path(GH_HOSTS_YML).expanduser()


def get_user(session):
    """Retrieve handle of logged in user."""
    response = session.get("https://api.github.com/user")
    response.raise_for_status()
    user_data = response.json()

    user = user_data["login"]
    return user


def get_review_requests(session):
    """Retrieve Pull Requests with Review Requests.

    Returns:
        dict: json object from api.

    """
    user = get_user(session)

    params = {"q": f"is:open is:pr review-requested:{user} archived:false"}
    response = session.get("https://api.github.com/search/issues", params=params)
    response.raise_for_status()
    return response.json()


def load_config(config_file):
    """Convert YAML file into Python Object."""
    config_text = config_file.read_text()
    config = yaml.safe_load(config_text)
    return config


def get_token(token, gh_config, hub_config):
    """Extract authentication token from CLI configuration file.

    Short circuit if a token is specified. Supported CLI configurations are:

    * gh
    * hub

    """
    if token:
        return token
    elif gh_config.exists():
        config = load_config(gh_config)
        host = config["github.com"]
        token = host["oauth_token"]
        return token
    elif hub_config.exists():
        config = load_config(hub_config)
        first_host, *_ = config["github.com"]
        token = first_host["oauth_token"]
        return token
    else:
        raise ValueError("Missing config for gh or hub CLIs.")


def github_session(token):
    """Create HTTP session with authentication header."""
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github.v3+json;charset=utf-8",
            "Authorization": f"token {token}",
        }
    )
    return session


def get_review_requests_defaults():
    """Return review requests data using default token resolution."""
    token = get_token(GITHUB_API_TOKEN, GH_CONFIG_FILE, HUB_CONFIG_FILE)
    session = github_session(token)

    data = get_review_requests(session)
    return data


def main():
    """Use the GitHub API to print Pull Requests with review requests."""
    token = get_token(GITHUB_API_TOKEN, GH_CONFIG_FILE, HUB_CONFIG_FILE)
    session = github_session(token)

    data = get_review_requests_defaults()

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
