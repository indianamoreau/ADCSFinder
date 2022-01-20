import click
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

@click.command()
@click.argument('targets', type=str)
@click.option("-t", "--timeout", default=3, type=int, help="Timeout for requests")
def run(targets, timeout):
    """Simple program that will check each of the IPs in the target list and find all the AD CS servers."""
    valid = []
    with open(targets) as f:
        for target in f.read().splitlines():
            try:
                try:
                    if requests.get(f"http://{target}/certsrv/", verify=False, timeout=timeout).status_code == 401:
                        # Check to ensure that this only happens for certsrv, else fasle positive
                        falsePositiveCheck = requests.get(f"http://{target}/certsrnotreal/", verify=False, timeout=timeout)
                        if falsePositiveCheck.status_code != 401:
                            valid.append(target)
                            click.secho(f"CA Server Found: {target}", fg="green")
                except:
                    pass
                if requests.get(f"https://{target}/certsrv/", verify=False, timeout=timeout).status_code == 401:
                    # Check to ensure that this only happens for certsrv
                    falsePositiveCheck = requests.get(f"https://{target}/certsrnotreal/", verify=False, timeout=timeout)
                    if falsePositiveCheck.status_code != 401:
                        valid.append(target)
                        click.secho(f"CA Server Found: {target}", fg="green")
                else:
                    click.secho(f"Not CA Server: {target}", fg="red")
            except Exception as e:
                click.secho(f"Error : {target} > {e}", fg="red")
        click.echo(f"Found {len(valid)} CA servers:")
        for ca in valid:
            click.echo(ca)


if __name__ == '__main__':
    run()
