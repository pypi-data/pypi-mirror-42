import logging

import click

from sagecreator.configurator import Configurator
from sagecreator.provisioner import Provisioner

logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
log = logging.getLogger(__name__)

configurator = Configurator()


@click.group()
def cli():
    pass


def valid_instance_type(ctx, param, value):
    valid_types = configurator.get_valid_instance_types()
    if value not in valid_types:
        raise click.BadParameter("Invalid instance type {}. Should be one of {}".format(value, str(valid_types)))
    return value


@cli.command(help="Configure infrastructure settings")
@click.option('--aws_access_key', prompt=True, required=True)
@click.option('--aws_secret_key', prompt=True, required=True, hide_input=True, confirmation_prompt=True)
@click.option('--company', prompt=True, required=True, help="Company name")
@click.option('--owner', prompt=True, required=True, help="Owner / Team that owns the service")
@click.option('--service', prompt=True, required=True, help="Name of the service")
@click.option('--instance_type', prompt=True, default="t3.micro", help="AWS instance type (default t3.micro)", callback=valid_instance_type)
@click.option('--spot_price', prompt=True, default=0.1, help="Price of the spot instance (default $0.1)")
@click.option('--cluster_size', prompt=True, default=1, help="Size of the cluster (default 1)")
def configure(aws_access_key, aws_secret_key, company, owner, service, instance_type, spot_price, cluster_size):
    try:
        configurator.persist(aws_access_key, aws_secret_key, company, owner, service, instance_type, spot_price, cluster_size)
    except Exception as e:
        log.error("Failed to store configuration. {}".format(str(e)))


@cli.command(help="Provision instance(s)")
def provision():
    try:
        click.echo("Provisioning based on {}".format(configurator.get_config_path()))
        prov = Provisioner(configurator)
        prov.provision()
    except Exception as e:
        log.error("Failed to provision instance(s). {}".format(str(e)))


@cli.command(help="Terminate instance(s)")
@click.option('--service', prompt=True, required=True, help="Name of the service")
def terminate(service):
    click.echo("Terminating {} service".format(service))
    prov = Provisioner(configurator)
    prov.terminate()


@cli.command(help="Full path to configuration file")
def pwd():
    click.echo(configurator.get_config_path())


if __name__ == "__main__":
    cli()
