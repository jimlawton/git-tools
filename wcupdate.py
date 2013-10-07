#!/usr/bin/python2
import sys
import git
import re
import os

if len(sys.argv) < 2:
    TOP = os.getcwd()
else:    
    TOP = sys.argv[1]

for dirname in sorted(os.listdir(TOP)):
    path = os.path.join(TOP, dirname)
    try: 
        repo = git.Repo(path)
    except git.errors.InvalidGitRepositoryError:
        continue
    try: 
        print "Updating %s..." % (dirname)
        repo.git.pull()
    except git.errors.GitCommandError:
        print "Error: could not update %s!" % (dirname)
        continue
