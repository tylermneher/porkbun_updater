# porkbun_updater
 This repo provides a command line tool to interact with porkbun dns api to update the dns records of a domain.
 
# Installation
The repo uses pdm for dependency management
Install pdm
```
pip install pdm
```
Then install deps and/or create a venv
```
pdm install
```

# Usage
The tool provides the following commands
```bash
python3 porkbun_updater/main.py
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Porkbun DNS Updater CLI

Options:
  --help  Show this message and exit.

Commands:
  check-auth              Check API authentication.
  config                  Configure API keys and domain.
  get-host-public-ip      Retrieve the host's public IP address.
  get-records             Retrieve DNS records by type.
  set-dns-record-by-type  Set or update a DNS record by type.
```
Setup the credentials:
```bash
python3 porkbun_updater/main.py config
```
Update your crontab with something like
```bash
*/5 * * * * cd ~/porkbun_updater && ./cron.sh
```