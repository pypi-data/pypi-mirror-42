import click
from awsecs import *

@click.command()
@click.option('--profile',help='Enter profile',default='default')
@click.option('--d',help='Enter days',default=0)
@click.option('--h',help='Enter hours',default=0)
@click.option('--m',help='Enter minutes',default=10)
@click.option('--cpuwarn',help='Enter the CPU usage limit',default=100)
@click.option('--memwarn',help='Enter the Memory usage limit',default=100)
def main(profile, cpuwarn, memwarn, d,h,m):
	obj.awsECS(profile, cpuwarn, memwarn, d,h,m)


if __name__=="__main__":
	main()