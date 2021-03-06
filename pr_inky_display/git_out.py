#!/home/pi/.local/share/virtualenvs/github_pull_requests-6hmCc7eu/bin/python
# -*- coding: utf-8 -*-
"""Print GitHub Pull Requests to InkyWHAT."""
import time
from urllib.parse import urlparse

from fonts.otf import ConnectionIII
from fonts.ttf import FredokaOne, Roboto

# from inky import InkyMockWHAT as InkyWHAT
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont
from tabulate import tabulate

from pr_inky_display.git_requests import get_review_requests_defaults

FIRA_CODE = "/home/pi/github/FiraCode/distr/ttf/FiraCode-Regular.ttf"
FONT = FIRA_CODE
FONT_SIZE = 10

FONT_TITLE = FredokaOne
FONT_TITLE_SIZE = 25

COLOUR = "red"
INKY_DISPLAY = InkyWHAT(COLOUR)


def get_pull_request_grid():
    """Create grid table of Pull Request information."""
    data = get_review_requests_defaults()

    pull_requests = []

    for pull_request in data["items"]:
        # "repository_url": "https://api.github.com/repos/Upgradetechops/terraform_modules",
        parsed = urlparse(pull_request["repository_url"])
        *_, org, repo = parsed.path.split("/")

        row = {
            "org": org,
            "repo": repo,
            # 'url': f'{org}/{repo}',
            # 'user': pull_request['user']['login'],
            "number": pull_request["number"],
            "title": pull_request["title"],
        }

        pull_requests.append(row)

    grid = tabulate(pull_requests, headers="keys")  # , showindex=True)
    print(grid)
    return grid


def main():
    """Display open Pull Requests with Review Request on the InkyWHAT."""
    width = INKY_DISPLAY.WIDTH
    height = INKY_DISPLAY.HEIGHT
    middle = width / 2

    font = ImageFont.truetype(FONT, FONT_SIZE)
    font_title = ImageFont.truetype(FONT_TITLE, FONT_TITLE_SIZE)

    title_text = "Pull Requests"
    title_width, title_height = font_title.getsize(title_text)
    title_x = middle - (title_width / 2)
    title_coordinates = (title_x, 0)

    title_background_height = title_height + 4
    title_background_coordinates = [0, 0, width, title_background_height]

    grid_coordinates = (5, title_background_coordinates[3] + 5)

    previous_grid = None

    title_background = INKY_DISPLAY.WHITE
    title_color = INKY_DISPLAY.RED

    while True:
        grid = get_pull_request_grid()
        if grid == previous_grid:
            time.sleep(20)
            continue
        else:
            previous_grid = grid

        img = Image.new("P", (width, height))
        draw = ImageDraw.Draw(img)

        title_background, title_color = title_color, title_background

        draw.rectangle(title_background_coordinates, fill=title_background)
        draw.text(title_coordinates, "Pull Requests", fill=title_color, font=font_title)

        draw.text(grid_coordinates, grid, fill=INKY_DISPLAY.BLACK, font=font)

        # Display the completed canvas on Inky wHAT

        INKY_DISPLAY.set_image(img)
        INKY_DISPLAY.show()
        # INKY_DISPLAY.wait_for_window_close()


if __name__ == "__main__":
    main()
