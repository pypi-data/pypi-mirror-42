# -*- coding: utf-8 -*-

"""Console script for tempest-zigzag."""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import click
import sys
from tempest_zigzag.tempest_zigzag import TempestZigZag
from tempest_zigzag.tempest_testcase_xml import TempestXMLAccessError


# ======================================================================================================================
# Main
# ======================================================================================================================
@click.command()
@click.argument('junit_input_file', type=click.Path(exists=True))
@click.argument('test_list', type=click.Path(exists=True))
@click.argument('config_file', type=click.Path(exists=True))
def main(junit_input_file, test_list, config_file):
    """Process multiple files created by tempest into a single accurate junit xml artifact"""
    try:
        click.echo(str(TempestZigZag.process_xml(junit_input_file, test_list, config_file)))
    except(TempestXMLAccessError, Exception) as e:
        click.echo(click.style(str(e), fg='red'))
        click.echo(click.style("\nFailed!", fg='red'))

        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover
