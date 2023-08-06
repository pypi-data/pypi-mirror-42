import click
from .config import Config
from apis import auth as auth_api

pass_config = click.make_pass_decorator(Config, ensure=True)

# login
@click.command('login')
@click.option('username', '-u','--username', help='username', required=True)
@click.option('password', '-p','--password', help='password', required=True)
@click.option('url', '--url', help='ucp url', required=True)
@pass_config
def login(config, username, password, url):
    config.set_username(username)
    config.set_url(url)
    verify_tls=False
    login_response = auth_api.login(url, username, password)
    if login_response == None:
        return
    else:
        print("Login Succeeded")
    auth_token = login_response.auth_token
    config.set_authtoken(auth_token)

    bundle_file = auth_api.clientbundle(url, auth_token)
    config.save_bundle_file(bundle_file)

# eval
@click.command('env')
def env():
    click.echo('pushd $(pwd) && cd ~/.ucp/bundle && eval "$(<env.sh)" && popd')
     