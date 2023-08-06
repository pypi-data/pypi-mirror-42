# import wpc

import click

# from .client import client
# from .work import work
# from .invoice import invoice
# from .config import config
from wpc.cli import customer, work, invoice, config, payment, report


@click.group()
def cli_commands():
    """
    Command line interface for wpc.


    Luca Parolari <luca.parolari23@gmail.com>

    Work Pay Calculator @ 2018
    """
    pass


cli_commands.add_command(config)
cli_commands.add_command(customer)
cli_commands.add_command(work)
cli_commands.add_command(report)
cli_commands.add_command(invoice)
cli_commands.add_command(payment)



