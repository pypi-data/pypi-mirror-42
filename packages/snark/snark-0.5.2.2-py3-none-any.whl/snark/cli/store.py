import click
from snark.log import logger
from snark.client.hyper_control import HyperControlClient
from snark.client.store_control import StoreControlClient
import yaml
from os import walk
import pprint
from tabulate import tabulate
import json
import os

def get_all_files(path = "./"):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.append((dirpath, dirnames, filenames))
        #break
    #print(f)
    return f

@click.command()
@click.argument('source', default='')
@click.argument('target', default='')
@click.option('--reset', flag_value=bool, default=False, help='reset credentials')
@click.pass_context
def sync(ctx, source, target, reset):
    """ Synchronizes files with Snark Storage """
    StoreControlClient().s3cmd('sync', source, target, reset=reset)

@click.command()
@click.argument('source', default='snark://')
@click.option('--reset', flag_value=bool, default=False, help='reset credentials')
@click.pass_context
def ls(ctx, source, reset):
    """ List files of a specific folder """
    StoreControlClient().s3cmd('ls', source, reset=reset)

@click.command()
@click.argument('source', default='')
@click.argument('target', default='')
@click.option('--recursive', '-r', flag_value=bool, default=False, help='recursive upload')
@click.option('--reset', flag_value=bool, default=False, help='reset credentials')
@click.pass_context
def cp(ctx, source, target, recursive, reset):
    """ Copy files from/to Snark Storage """
    cmd = ''
    if 'snark://' in source:
        cmd = 'get'
    if 'snark://' in target:
        cmd = 'put'
    if 'snark://' in source and 'snark://' in target:
        cmd = 'cp'
    cmd = 'cp'
    StoreControlClient().s3cmd(cmd, source, target, recursive=recursive, reset=reset)

@click.command()
@click.argument('source', default='')
@click.option('--recursive', '-r', flag_value=bool, default=False, help='recursive upload')
@click.option('--reset', flag_value=bool, default=False, help='reset credentials')
@click.pass_context
def rm(ctx, source, recursive, reset):
    """ Remove files from Snark Storage """
    StoreControlClient().s3cmd('rm', source, recursive=recursive)

@click.command()
@click.argument('source', default='')
@click.argument('target', default='')
@click.option('--recursive', '-r', flag_value=bool, default=False, help='recursive upload')
@click.option('--reset', flag_value=bool, default=False, help='reset credentials')
@click.pass_context
def mv(ctx, source, target, recursive, reset):
    """Move files in Snark Storage """
    StoreControlClient().s3cmd('mv', source, target,  recursive=recursive, reset=reset)
