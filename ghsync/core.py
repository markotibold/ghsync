#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO Add token support as described in gihub3.py examples
# http://github3py.readthedocs.org/en/latest/examples/oauth.html


"""Kenneth Reitz's GitHub Syncer

This script uses the GitHub API to get a list of all forked, mirrored, public,
and private repos in your GitHub account - and of the organizations you belong to.
If the repo already exists locally, it will update it via git-pull. Otherwise, it 
will properly clone the repo.

It will organize your repos into the following directory structure:

<repo_owner>
            /<repo_name>

Requires Ian Cordasco's github3.py (http://pypi.python.org/pypi/github3.py).

Inspired by Gisty (http://github.com/swdyh/gisty).

"""

import os
import sys
import subprocess
import getpass
from clint import args
from clint.textui import puts, colored
from github3 import GitHub, GitHubError

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
    GITHUB_PASSWORD = getpass.getpass('Type in your Github password: ')

    upstream_on = args.flags.contains('--upstream')
    organization = args.grouped.get('-o', None)
    organization = organization and organization[0]

    os.chdir(GHSYNC_DIR)

    # API Object
    github = GitHub(login=GITHUB_USER, password=GITHUB_PASSWORD)
    try:
        github.iter_repos().next()
    except GitHubError:
        sys.exit('Authentication failed')
    # Build the list of repositories
    repos = []

    if not organization:
        repos.extend(github.iter_repos())  # all repos owned by you, either your's originals or forked
        for org in github.iter_orgs():
            repos.extend(org.iter_repos())  # all repos owned by all organizations you belong to
    else:  # Only clone / pull repos that belong to organization
        repos.extend(github.organization(organization).iter_repos())

    for i, repo in enumerate(repos):
        print i + 1
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
            subprocess.call('git pull', shell=True)

            if is_fork and upstream_on:
                #print repo.__dict__
                puts(colored.red(
                    'Adding upstream: {0.parent}'.format(repo)))
                subprocess.call('git remote add upstream {0}'.format(
                    repo.parent.git_url
                    ), shell=True)

            os.chdir('..')

        else:
            if is_private:
                puts(colored.red(
                'Cloning private repo: {repo.name}'.format(
                    repo=repo)))
                subprocess.call('git clone {0}'.format(repo.ssh_url), shell=True)
                print('git clone {0}'.format(repo.ssh_url))

                if is_fork and upstream_on:
                    os.chdir(repo.name)
                    puts(colored.red('Adding upstream: {0}'.format(
                        repo.parent.name
                        )))
                    subprocess.call('git remote add upstream {0}'.format(
                        repo.parent.git_url
                        ), shell=True)
                    os.chdir('..')

            else:
                puts(colored.red('Cloning repo: {repo.name}'.format(
                    repo=repo)))
                subprocess.call('git clone {0}'.format(repo.git_url), shell=True)
                print ('git clone {0}'.format(repo.git_url))

        # return to base
        os.chdir('..')

if __name__ == '__main__':
    run()
