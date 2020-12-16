# Pull Requests InkyWHAT Display

Poll the GitHub API for a list of Pull Requests where you are added as a
Reviewer. When a change in the Pull Requests is detected, the InkyWHAT display
will be refreshed.

## Requirements

### Pimoroni Inky Setup

#### Pimoroni Automated Setup

The automated installation provided by Pimoroni is really good about setting up
a Raspberry Pi with everything.

```bash
curl https://get.pimoroni.com/inky | bash
```

#### Manual Setup

##### SPI

Enable the SPI pins for the Raspberry Pi GPIO.

```bash
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint get_spi  # Should return 0, 1 means disabled
```

##### Numpy Libraries

These base library packages are required to run a `numpy` in a proper Pipenv.
If you are using `python3-numpy` provided by the system package manager, then
these should not be needed.

```bash
sudo apt install -y \
  libatlas-base-dev \
  libopenjp2-7 \
  libtiff5
```

### GitHub Authentication

The code can use the configuration files for `gh` or `hub` CLIs.
Configuration using one of the CLIs is recommended for ease of use and added
functionality outside of this application. The environment variable
`GITHUB_API_TOKEN` is also supported.

Choose one of the following ways to authenticate with GitHub to get an
authentication token.

#### Install `gh` CLI

Install the official GitHub CLI from https://cli.github.com/ and follow the
web authentication workflow.

#### Install `hub` CLI

Install the unofficial `hub` CLI from https://hub.github.com/ and follow the
web authentication workflow.

#### Manually Create Personal Access Token

1. Go to https://github.com/settings/tokens
1. Generate a new token with permissions:

    * repo

1. Export the environment variable or use a
  [.env](https://pipenv-fork.readthedocs.io/en/latest/advanced.html#automatic-loading-of-env)
  file with the variable:

    ```bash
    GITHUB_API_TOKEN=293lj23l4kj2lk4j3223k4j
    ```

## Running

Install Pipenv and create the virtual environment.

```bash
pip3 install pipenv
pipenv install --sequential --skip-lock  # Flags help speed this up slightly
```

Enter the virtual environment and run the scripts:

```bash
pipenv shell

(env) git-pr-inky
(env) python -m pr_inky_display.git_out  # alternative

(env) git-requests
(env) python -m pr_inky_display.git_requests  # alternative
```

Or use the Pipenv command to run:

```bash
pipenv run ./pr_inky_display/git_out.py
pipenv run ./pr_inky_display/git_requests.py
```

Or update the shebang line to use the virtual environment Python executable.

```bash
pipenv --venv
/home/pi/.local/share/virtualenvs/pull_requests_inky_display-ur2-XW38
```

```python
#!/home/pi/.local/share/virtualenvs/pull_requests_inky_display-ur2-XW38/bin/python
```

And make sure the application is marked as executable.

```bash
chmod +x pr_inky_display/git_out.py
./pr_inky_display/git_out.py
```

## Automated Running With Systemd

Install and enable the Systemd Service:

```bash
cp pull_requests.services ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable pull_requests
```

And make sure to allow for your user to run without needing an initial login
session. Without this, you will need to SSH to the machine before the Service
will start.

```bash
sudo loginctl enable-linger pi
```
