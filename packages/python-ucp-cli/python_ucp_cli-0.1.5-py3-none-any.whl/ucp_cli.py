import click
import commands.config as Config
import commands.auth as auth

pass_config = click.make_pass_decorator(Config.Config, ensure=True)

@click.group()
@click.option('--insecure-tls', is_flag=True)
@pass_config
def cli(config, insecure_tls):
    config.insecure_tls = insecure_tls
    pass

cli.add_command(auth.login)
cli.add_command(auth.env)

if __name__ == '__main__':
    cli()