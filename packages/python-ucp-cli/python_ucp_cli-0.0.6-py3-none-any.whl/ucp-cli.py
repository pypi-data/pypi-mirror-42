import click
import requests
import json
import subprocess
import os
import tempfile
import shutil
import zipfile

requests.packages.urllib3.disable_warnings() 

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--insecure-tls', is_flag=True)
@pass_config
def cli(config, verbose, insecure_tls):
    config.verbose = verbose
    config.insecure_tls = insecure_tls
    if verbose:
        click.echo('We are in verbose mode.')

def get_ucpdir(file_path=os.path.expanduser('~')):
    ucp_dirpath = file_path+'/.ucp'
    directory = os.path.dirname(ucp_dirpath)
    if not os.path.exists(ucp_dirpath):
        os.makedirs(ucp_dirpath)
        return ucp_dirpath
    return ucp_dirpath

def get_auth_token(url, username, password, verify_tls):
    """Get authtoken from UCP"""
    payload = {"username": username, "password": password}
    r = requests.post(url + '/auth/login', json=payload, verify=verify_tls)
    r_json = json.loads(r.text)
    auth_token = r_json['auth_token']
    return auth_token

def save_auth_token(auth_token, login_dir=get_ucpdir()):
    auth_token_path=login_dir + "/auth_token"
    with open(auth_token_path, "w+") as auth_file:
        auth_file.write(auth_token)

def ensure_auth_token(login_dir=get_ucpdir()):
    auth_token_path = login_dir + "/auth_token"
    f = open(auth_token_path, "r")
    if not os.path.exists(auth_token_path):
        print("Please login to ucp")
    else:
        auth_token = f.read()
        return auth_token

def get_bundle_file(url, auth_token, verify_tls):
    headers = {'Authorization': ("Bearer %s" % (auth_token))}
    full_url = url + '/api/clientbundle'
    response = requests.get(full_url, headers=headers, verify=verify_tls)
    return response

def save_bundle_file(response, login_dir=get_ucpdir()):
   bundle_file_path=login_dir+'/bundle.zip'
   with open(bundle_file_path, 'wb') as out_file:
    out_file.write(response.content)
   del response

def unpack_bundle(login_dir=get_ucpdir()):
   bundle_file_path=login_dir+'/bundle.zip'
   bundle_unpack_dir=login_dir+'/bundle'
   if not os.path.exists(bundle_unpack_dir):
     os.makedirs(bundle_unpack_dir)
   archive = zipfile.ZipFile(bundle_file_path)
   archive.extractall(bundle_unpack_dir)
 
@cli.command()
@click.option('--username', '-u', help='Username to UCP', required=True)
@click.option('--password', '-p', help='Password to UCP', required=True)
@click.option('--url', help='The Url to a UCP Manager', required=True)
@pass_config
def login(config, username, password, url):
    """Log in to UCP"""
    auth_token = get_auth_token(url, username, password, config.insecure_tls)
    save_auth_token(auth_token)
    r = get_bundle_file(url, auth_token, config.insecure_tls)
    save_bundle_file(r)

@cli.command()
def env():
    """echo load env"""
    click.echo('pushd $(pwd) && cd ~/.ucp/bundle && eval "$(<env.sh)" && popd')
 