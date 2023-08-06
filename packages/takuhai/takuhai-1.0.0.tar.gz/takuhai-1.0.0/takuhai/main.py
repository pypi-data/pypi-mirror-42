import click

import takuhai
from takuhai.serve import serve


@click.command()
@click.option('--host', '-h', default='localhost', help='Host name.')
@click.option('--port', '-p', default=8000, help='Port number.')
@click.option('--open_url', '-o', is_flag=True, help='Open default browser.')
@click.option('--absolute', '-a', is_flag=True, help='Set absolute URLs.')
@click.option('--version', is_flag=True, help='Show version.')
def cli(host, port, open_url, absolute, version):
    if version:
        print('takuhai version:', takuhai.__version__)
        return
    serve(host, port, open_url, not absolute)


def main():
    cli()


if __name__ == '__main__':
    main()
