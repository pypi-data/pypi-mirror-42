"""
Entrypoint for the bbcli tool
"""

from contextlib import suppress
from distutils.util import strtobool
from os import makedirs, path
from shutil import which
from subprocess import CalledProcessError, check_call, check_output

import click

HUB_VERSION = '2.10.0'
REPODIR = path.abspath('repostash_bbdeploy')
REPOS = [
    'brewblox-devcon-spark',
    'brewblox-history',
    'brewblox-mdns',
    'brewblox-ui',
    'brewblox-ctl-lib',
    'brewblox-firmware',
]


def confirm(question):
    print('{} [Y/n]'.format(question))
    while True:
        try:
            return bool(strtobool(input().lower() or 'y'))
        except ValueError:
            print('Please respond with \'y(es)\' or \'n(o)\'.')


def create_repos():
    makedirs(REPODIR, exist_ok=True)
    [
        check_output(f'git clone --no-checkout https://github.com/BrewBlox/{repo}.git', shell=True, cwd=REPODIR)
        for repo in REPOS
        if not path.exists(f'{REPODIR}/{repo}/.git')
    ]


def install_hub():
    [
        check_output(cmd, shell=True)
        for cmd in [
            f'wget https://github.com/github/hub/releases/download/v{HUB_VERSION}/hub-linux-amd64-{HUB_VERSION}.tgz',
            f'tar zvxvf hub-linux-amd64-{HUB_VERSION}.tgz',
            f'sudo ./hub-linux-amd64-{HUB_VERSION}/install',
            f'rm -rf hub-linux-amd64-{HUB_VERSION}*',
        ]
    ]


@click.group()
def cli():
    create_repos()
    if not which('hub') and confirm('hub cli not found - do you want to install it?'):
        install_hub()


@cli.command()
def delta():
    headers = ['repository'.ljust(25), 'develop >', 'edge >', 'tag']
    print(*headers)
    print('-' * len(' '.join(headers)))  # will include separators added by print()
    for repo in REPOS:
        check_output('git fetch --tags',
                     shell=True,
                     cwd=f'{REPODIR}/{repo}')
        dev_edge = check_output(
            'git rev-list --count origin/edge..origin/develop',
            shell=True,
            cwd=f'{REPODIR}/{repo}').decode().rstrip()
        edge_tag = check_output(
            'git rev-list --count $(git describe --tags $(git rev-list --tags --max-count=1))..origin/edge',
            shell=True,
            cwd=f'{REPODIR}/{repo}').decode().rstrip()
        vals = [repo, dev_edge, edge_tag, '-']
        print(*[v.ljust(len(headers[idx])) for idx, v in enumerate(vals)])


@cli.command()
def release():
    for repo in REPOS:
        if not confirm(f'Do you want to create a develop -> edge PR for {repo}?'):
            continue

        with suppress(CalledProcessError):
            check_call(
                'hub pull-request -b edge -h develop -m "edge release"',
                shell=True,
                cwd=f'{REPODIR}/{repo}')


if __name__ == '__main__':
    cli()
