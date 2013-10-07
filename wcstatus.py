#!/usr/bin/python2
import sys
import git
import os
import re

if len(sys.argv) < 2:
    TOP = os.getcwd()
else:    
    TOP = os.path.abspath(sys.argv[1])

RE_UNTRACKED = re.compile(r"# Untracked files:")
RE_UNSTAGED = re.compile(r"# Changes not staged for commit:")
RE_UNCOMMITTED = re.compile(r"# Changes to be committed:")
RE_UNPUSHED = re.compile(r"# Your branch is ahead of '.*' by [0-9]+ commits?\.")

def hasUntracked(repo):
    return bool(RE_UNTRACKED.search(repo.git.status()))

def hasUnstaged(repo):
    return bool(RE_UNSTAGED.search(repo.git.status()))

def hasUncommitted(repo):
    return bool(RE_UNCOMMITTED.search(repo.git.status()))

def hasUnpushed(repo):
    return bool(RE_UNPUSHED.search(repo.git.status()))

def hasChanges(repo):
    if hasUntracked(repo) or hasUnstaged(repo) or hasUncommitted(repo) or hasUnpushed(repo):
        return True
    return False

def printChanges(repo, path):
    text = "%s: " % path
    if hasChanges(repo):
        if hasUntracked(repo):
            text += "untracked"
        if hasUnstaged(repo):
            text += ", unstaged"
        if hasUncommitted(repo):
            text += ", uncommitted"
        if hasUnpushed(repo):
            text += ", unpushed"
    print text

for dirname in sorted(os.listdir(TOP)):
    path = os.path.join(TOP, dirname)
    try: 
        repo = git.Repo(path)
    except git.errors.InvalidGitRepositoryError:
        continue
    if hasChanges(repo):
        printChanges(repo, dirname)
