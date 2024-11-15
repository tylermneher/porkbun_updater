# porkbun_updater
- Clone the repo
- Install deps `pdm install` or `pip install requests click`
- Run config `python porkbun_updater/main.py config`
- install a crontab with a command like `python porkbun_updater/main.py set-dns-record-by-type --record-type A`
click auto help
```
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