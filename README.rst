ghsync: GitHub Repo Syncer
==========================

This script uses the GitHub API to get a list of all forked, mirrored, public,
and private repos in your GitHub account. If the repo already exists locally,
it will update it via git-pull. Otherwise, it will properly clone the repo.

It will organize your repos into the following directory structure:

<repo_owner>
            /<repo_name>

Requires Ian Cordasco's github3.py (http://pypi.python.org/pypi/github3.py).

Inspired by Gisty (http://github.com/swdyh/gisty).


Install
-------

To install ghsync, simply run: ::

    $ pip install ghsync

The command ``ghsync`` will then be available to you from the command
line. Beware, unless you set the ``GHSYNC_DIR`` environment variable, it
will add all the repos to your current directory.::

    $ export GHSYNC_DIR='~/repos/'

Github
------

Store you github login globally:

    git config --global github.user "your_user_name"


Options
-------

If the ``--upsteam`` argument is passed, all forked repos will have an
**upstream** remote added, pointing to their parent repo on GitHub.

You can also selectively sync certian repos with ``-o <organization_name>``. If
you'd like to only sync repositories that belong to that organization (provided you have access 
to their repos), for example::

    $ ghsync -o acme

Tips
----

When running on linux, you may want to run these commands to make sure
you don't have to authenticate to Github on every clone/pull and enter your
passphrase. Note that you could have also created an ssh-key with an empty 
passprase but that obviously is not safe.::

    ssh-agent /bin/bash
    ssh-add

Or use this method from Github's docs:
    
    git config --global credential.helper cache
    # Set git to use the credential memory cache (for 15 minutes)

Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your
changes to the **develop** branch (or branch off of it), and send a pull
request.


.. _`the repository`: http://github.com/kennethreitz/ghsync
