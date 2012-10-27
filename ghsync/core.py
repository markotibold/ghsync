#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO Add token support as described in gihub3.py examples
# http://github3py.readthedocs.org/en/latest/examples/oauth.html


"""Kenneth Reitz's GitHub Syncer

This script uses the GitHub API to get a list of all forked, mirrored, public,
and private repos in your GitHub account. If the repo already exists locally,
it will update it via git-pull. Otherwise, it will properly clone the repo.

It will organize your repos into the following directory structure:

repo owner 1
            /repo name
repo owner 2
            /repo name

Requires Ian Cordasco's github3.py (http://pypi.python.org/pypi/github3.py).

Inspired by Gisty (http://github.com/swdyh/gisty).
"""

import os
import getpass
from clint import args
from clint.textui import puts, colored
from github3 import GitHub

try:
    # check_output is new in 2.7.
    from subprocess import check_output

    def cmd(command):
        return check_output(command, shell=True).strip()
except ImportError:
    # commands is deprecated and doesn't work on Windows
    from commands import getoutput as cmd


__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = '2011 Kenneth REitz'
__version__ = '0.3.1'

# GitHub configurations
GITHUB_USER = cmd('git config github.user')
GHSYNC_DIR = os.environ.get('GHSYNC_DIR', '.')


def run():
    # cli flags
    GITHUB_PASSWORD = args.grouped.get('-p', None)
    if not GITHUB_PASSWORD:
        GITHUB_PASSWORD = getpass.getpass('Type in your Github password: ')
    else:
        GITHUB_PASSWORD = GITHUB_PASSWORD[0]

    upstream_on = args.flags.contains('--upstream')
    organization = args.grouped.get('-o', None)
    organization = organization and organization[0]

    os.chdir(GHSYNC_DIR)

    # API Object
    github = GitHub(login=GITHUB_USER, password=GITHUB_PASSWORD)

    # repo slots
    repos = []

    if not organization:
        repos.extend(github.list_repos())  # all repos owned by you, either your's originals or forked
        for org in github.list_orgs():
            repos.extend(org.list_repos())  # all repos owned by all organizations you belong to
    else:
        repos.extend(github.organization(organization).list_repos())

    for repo in repos:

        # create repo_owner directory (safely)
        try:
            os.makedirs(repo.owner.login)
        except OSError:
            pass

        # enter owner dir
        os.chdir(repo.owner.login)

        # I own the repo
        is_private = repo.is_private()
        is_fork = repo.is_fork()

        # just `git pull` if it's already there
        if os.path.exists(repo.name):

            os.chdir(repo.name)
            puts(colored.red('Updating repo: {0.name}'.format(repo)))
            os.system('git pull')

            if is_fork and upstream_on:
                #print repo.__dict__
                puts(colored.red(
                    'Adding upstream: {0.parent}'.format(repo)))
                os.system('git remote add upstream {0}'.format(
                    repo.parent.git_url
                    ))

            os.chdir('..')

        else:
            if is_private:
                puts(colored.red(
                'Cloning private repo: {repo.name}'.format(
                    repo=repo)))
                os.system('git clone {0}'.format(repo.ssh_url))
                print('git clone {0}'.format(repo.ssh_url))

                if is_fork and upstream_on:
                    os.chdir(repo.name)
                    puts(colored.red('Adding upstream: {0}'.format(
                        repo.parent.name
                        )))
                    os.system('git remote add upstream {0}'.format(
                        repo.parent.git_url
                        ))
                    os.chdir('..')

            else:
                puts(colored.red('Cloning repo: {repo.name}'.format(
                    repo=repo)))
                os.system('git clone {0}'.format(repo.git_url))
                print ('git clone {0}'.format(repo.git_url))

        # return to base
        os.chdir('..')

if __name__ == '__main__':
    run()
