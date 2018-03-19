import sqlite3
import sys
import os
from subprocess import call, check_output
from columns import Columns
from cd import cd

PROJECT = ''

if len(sys.argv) > 1:
  PROJECT = sys.argv[1]
else:
  print 'Give parameter (project name)'
  sys.exit()

PATH = 'DBs/' + PROJECT + '/parts'

folders = next(os.walk(PATH))[1]

for i in range(len(folders)):
  i += 1

  database = "%s/%i_part/%i_part.sqlite" % (PATH, i, i)
  conn = sqlite3.connect(database)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM commits;")
  commits = cursor.fetchall()
  qtd = len(commits)
  
  if (i == 1):
    firstCommitSHA = commits[qtd - 1][Columns.SHA.value]
    with cd("projects/" + PROJECT):
      call(["git", "checkout", firstCommitSHA, "-b", "interval_0_begin"])
      call(["git", "push", "-u", "origin", "HEAD"])
  lastCommitSHA = commits[0][Columns.SHA.value]
  with cd("projects/" + PROJECT):
    call(["git", "checkout", lastCommitSHA, "-b", "interval_" + str(i)])
    call(["git", "push", "-u", "origin", "HEAD"])