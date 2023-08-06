import sys
import click
from rotatekeys import *


@click.command()
@click.option('--file1',help='Blacklist file')
@click.option('--file2',help='Whitelist file')
@click.option('--profile',help='Enter profile',default='default')
@click.argument('file1',type=click.File('r'))
@click.argument('file2',type=click.File('r'))
def main(file1,file2,profile):
	obj.rotatekeys(file1,file2,profile)

if __name__=="__main__":
	main()