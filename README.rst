ghsync: GitHub Repo Syncer
==========================

This script uses the GitHub API to get a list of all forked, mirrored, public, and 
private repos in your GitHub account. If the repo already exists locally, it will 
update it via git-pull. Otherwise, it will properly clone the repo.

It will organize your repos into the following directory structure: ::

    + repos
      ├── forks    (public fork repos)
      ├── mirrors  (public mirror repos)
      ├── private  (private repos)
      ├── public   (public repos)
      ├── watched  (public watched repos)
      └── sync.py  (this script)

Requires Ask Solem's github2 (http://pypi.python.org/pypi/github2).

Inspired by Gisty (http://github.com/swdyh/gisty).



Contribute
----------

If you'd like to contribute, simply fork `the repository`_, commit your changes to the **develop** branch (or branch off of it), and send a pull request.


.. _`the repository`: http://github.com/kennethreitz/ghsync