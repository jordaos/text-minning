import sqlite3
import sys
import os
from cd import cd
from subprocess import call

PROJECT = ''
if len(sys.argv) > 1:
  PROJECT = sys.argv[1]
else:
  print 'Give parameter (project name)'
  sys.exit()

PATH = 'DBs/' + PROJECT + '/parts'
REPO_PATH = 'projects/' + PROJECT + '_parts'

folders = next(os.walk(PATH))[1]

for i in range(len(folders)):
  i += 1
  branch = "interval_%i" % i
  with cd(REPO_PATH):
    call(["git", "clone", "-b", branch, "--single-branch", "https://github.com/jordaos/" + PROJECT])
    call(["mv", PROJECT, branch])