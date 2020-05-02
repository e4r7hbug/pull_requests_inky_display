# Pull Requests InkyWHAT Display

Poll the GitHub API for a list of Pull Requests where you are added as a
Reviewer. When a change in the Pull Requests is detected, the InkyWHAT display
will be refreshed.

## Requirements

### Pimoroni Automated Setup

The automated installation provided by Pimoroni is really good about setting up
a Raspberry Pi with everything.

```bash
curl https://get.pimoroni.com/inky | bash
```

### Manual Setup

#### SPI

Enable the SPI pins for the Raspberry Pi GPIO.

```bash
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint get_spi  # Should return 0, 1 means disabled
```

#### Numpy Libraries

These base library packages are required to run a `numpy` in a proper Pipenv.
If you are using `python3-numpy` provided by the system package manager, then
these should not be needed.

```bash
sudo apt install -y \
  libatlas-base-dev \
  libopenjp2-7 \
  libtiff5
```

#### GitHub Hub

The Python code calls out to the `hub` command. Make sure to run the `hub`
command to set up authentication.

1. Install https://hub.github.com/
1. Try `hub api`

## Running

Install Pipenv and create the virtual environment.

```bash
pip3 install pipenv
pipenv install --sequential --skip-lock  # Flags help speed this up slightly
```

Enter the virtual environment and run the script:

```bash
pipenv shell
(env) ./git_out.py
```

Or use the Pipenv command to run:

```bash
pipenv run ./git_out.py
```

Or update the shebang line to use the virtual environment Python executable.

```python
#!/home/py/.local/share/virtualenvs/github_pull_requests-s3kjso/bin/python
```

And make sure the application is marked as executable.

```bash
chmod +x git_out.py
./git_out.py
```

## Automated Running With Systemd

Install and enable the Systemd Service:

```bash
cp github_pull_requests.services ~/.local/systemd/user/
systemctl --user daemon-reload
systemctl --user enable github_pull_requests
```

And make sure to allow for your user to run without needing an initial login
session. Without this, you will need to SSH to the machine before the Service
will start.

```bash
sudo loginctl enable-linger pi
```
