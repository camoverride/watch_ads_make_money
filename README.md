# Watch Ads Make Money!

## Setup

- `git clone git@github.com:camoverride/watch_ads_make_money.git`
- `cd watch_ads_make_money`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

Start a service with systemd. This will start the program when the computer starts and revive it when it dies:

- `mkdir -p ~/.config/systemd/user`
- `cat watch_ads.service > ~/.config/systemd/user/watch_ads.service`

Start the service using the commands below:

- `systemctl --user daemon-reload`
- `systemctl --user enable watch_ads.service`
- `systemctl --user start watch_ads.service`

Start it on boot:

- `sudo loginctl enable-linger $(whoami)`

Get the logs:

- `journalctl --user -u watch_ads.service`
