import click
from jvstats import Delays

@click.group()
def cli():
  ''' a command line tool for statistics '''
  return 0

@click.group()
def delays():
  ''' get statistics of delays '''
  return 0

@click.command()
@click.option('--width', default=3, help='maximum number of items to retrieve median from',  type=int)
@click.option('--filename', help='file to retrieve stats from, one statistic per line', type=click.File('r'))
def medians(width,filename):
  '''
  retrieve the median from either stdin or a file
  '''

  # we create a container for our delay statistics
  d=Delays(width=width)
  delay_lines=None

  # if a filename is given then check if it can be read
  if filename:
    try:
      delay_lines=[line for line in filename.readlines() if line.strip()]
    except Exception as exc:
      click.echo(exc,err=True)

  # otherwise check if we have a stream from stdin (e.g. from a pipe)
  elif not click.get_text_stream('stdin').isatty():
    stdin = click.get_text_stream('stdin').read()
    delay_lines = stdin.strip().splitlines()

  # check if we have any lines to check
  if delay_lines is not None:
    for line in delay_lines:
      try:
        delay=int(str(line).replace('\r', '').replace('\n', '').replace('^M',''))
        d.addDelay(delay)
        click.echo(d.medians[-1])
      except Exception as exc:
        click.echo("line:%s"%line,err=True)
        click.echo(exc,err=True)
    
cli.add_command(delays)
delays.add_command(medians)
