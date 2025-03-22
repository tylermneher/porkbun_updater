import logging
from pathlib import Path
from pprint import pprint
from typing import Union, Dict
import click
import requests
import json

import re

ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})$')

def is_valid_ipv4(ip):
    return bool(ipv4_pattern.match(ip))

PORKBUN_API_URL = "https://api.porkbun.com/api/json/v3/"

config_dir = Path(__file__).parent
key_filename = config_dir / '.porkbun_updater_api_keys.json'
config_filename = config_dir / '.porkbun_updater_config.json'

# Configure logging
log_filename = config_dir / 'porkbun_updater.log'
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def save_config_file(file_path: Path, data: Dict):
    """Helper function to save configuration files."""
    file_path.write_text(json.dumps(data))
    logging.info(f"Configuration saved to {file_path}")

@click.group()
def cli():
    """Porkbun DNS Updater CLI"""
    pass

@click.command()
@click.option('--api-key', prompt='API Key')
@click.option('--api-secret', prompt='API Secret Key')
@click.option('--domain', prompt='Domain')
def config(api_key, api_secret, domain):
    """Configure API keys and domain."""
    save_config_file(key_filename, {"apikey": api_key, "secretapikey": api_secret})
    save_config_file(config_filename, {'domain': domain})
    logging.info("Configuration command executed")

def get_auth_dict():
    """Retrieve authentication credentials from configuration."""
    try:
        return json.loads(key_filename.read_text())
    except FileNotFoundError:
        logging.error("API keys not found. Run `config` first.")
        click.echo("API keys not found. Run `config` first.")
        exit(1)

def get_domain_info():
    """Retrieve the domain information from configuration."""
    try:
        return json.loads(config_filename.read_text())['domain']
    except FileNotFoundError:
        logging.error("Domain config not found. Run `config` first.")
        click.echo("Domain config not found. Run `config` first.")
        exit(1)

def make_api_request(uri: str, request_body: Union[Dict, None] = None, verbose=False):
    """Make an authenticated request to the Porkbun API."""
    url = PORKBUN_API_URL + uri
    auth = get_auth_dict()
    if request_body:
        if verbose:
            logging.info(f"Request body: {request_body}")
        request_body.update(auth)
    else:
        request_body = auth
    try:
        response = requests.post(url, data=json.dumps(request_body))
        response.raise_for_status()
        if response.text:
            if verbose:
                logging.info(f"Response: {response.text}")
            return json.loads(response.text)
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        click.echo(f"API request failed: {e}")
        try:
            error_data = json.loads(response.text)
            pprint(error_data)
        except Exception:
            logging.error("Unable to parse error details.")
            click.echo("Unable to parse error details.")
        exit(1)

@click.command()
def check_auth():
    """Check API authentication."""
    response = make_api_request('ping')
    logging.info("Authentication successful!")
    click.echo("Authentication successful!")
    return response

@click.command()
def get_host_public_ip():
    """Retrieve the host's public IP address."""
    make_ip_address_request()

def make_ip_address_request():
    try:
        auth_response = make_api_request('ping')
        if 'yourIp' in auth_response:
            ip = auth_response['yourIp']
            if not is_valid_ipv4(ip):
                raise ValueError(f"Invalid IP address: {ip}")
            logging.info(f"Public IP (via Porkbun): {ip}")
            click.echo(f"Public IP (via Porkbun): {ip}")
            return ip
    except Exception:
        logging.error("Failed to retrieve IP from Porkbun API.")
        click.echo("Failed to retrieve IP from Porkbun API.")

    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        response.raise_for_status()
        ip = response.text.strip()
        logging.info(f"Public IP (via fallback): {ip}")
        click.echo(f"Public IP (via fallback): {ip}")
        return ip
    except requests.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        click.echo(f"Error fetching public IP: {e}")
        exit(1)

@click.command()
@click.option('--record-type', default='A', prompt='Record Type (e.g., A, CNAME)')
@click.option('--domain', default=lambda: get_domain_info())
@click.option('--sub-domain', default=None, help="Subdomain to filter records (optional).")
def get_records(record_type, domain, sub_domain):
    """Retrieve DNS records by type."""
    uri = f'dns/retrieveByNameType/{domain}/{record_type}'
    if sub_domain:
        uri += f"/{sub_domain}"
    records = make_api_request(uri)
    logging.info(f"Retrieved records: {records}")
    pprint(records)

@click.command()
@click.option('--record-type', default='A', prompt='Record Type (e.g., A, CNAME)')
@click.option('--domain', default=lambda: get_domain_info())
@click.option('--sub-domain', default=None, help="Specify the subdomain (optional).")
@click.option('--ip-address', default=lambda: make_ip_address_request(), help="IP address to set.")
@click.option('--ttl', default=600, help="Time-to-Live for the record.")
@click.option('--dry-run', is_flag=True, help="Simulate changes without applying them.")
def set_dns_record_by_type(record_type, domain, sub_domain, ip_address, ttl, dry_run):
    """Set or update a DNS record by type."""
    if dry_run:
        logging.info(
            f"[DRY RUN] Would update '{domain}' '{record_type}' record"
            f"{f' for subdomain {sub_domain}' if sub_domain else ''} "
            f"to '{ip_address}' with TTL {ttl}."
        )
        click.echo(
            f"[DRY RUN] Would update '{domain}' '{record_type}' record"
            f"{f' for subdomain {sub_domain}' if sub_domain else ''} "
            f"to '{ip_address}' with TTL {ttl}."
        )
        return
    uri = f'dns/editByNameType/{domain}/{record_type}/'
    if sub_domain:
        uri += f"{sub_domain}"
    request_body = {"content": ip_address, "ttl": int(ttl)}
    make_api_request(uri, request_body, verbose=True)
    logging.info(f"Updated '{domain}' '{record_type}' record to '{ip_address}' with TTL {ttl}.")

cli.add_command(config)
cli.add_command(check_auth)
cli.add_command(get_records)
cli.add_command(get_host_public_ip)
cli.add_command(set_dns_record_by_type)

if __name__ == '__main__':
    cli()