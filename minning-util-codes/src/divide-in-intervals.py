import sqlite3
import sys
import os
from columns import Columns
from subprocess import call, check_output
from cd import cd

PROJECT = ''
if len(sys.argv) > 1:
  PROJECT = sys.argv[1]
else:
  print 'Give parameter (project name)'
  sys.exit()

PATH = 'DBs/' + PROJECT
DB = PATH + "/" + PROJECT + '.sqlite'

def have_twohundred_commits(sha, lastVersionHave):
  with cd("projects/" + PROJECT):
    call(["git", "checkout", sha])
    qtdCommits = int(check_output(["ruby", "./../../src/count-commits.rb", "./../../projects/" + PROJECT]))
    call(["git", "reset", "--hard", "2.x"])
    if (((qtdCommits % 200) == 0 and qtdCommits > lastVersionHave) or (qtdCommits > lastVersionHave + 200)):
      return True
  return False

def save_db(n):
  database = "%s/parts/%i_part/%i_part.sqlite" % (PATH, n, n)
  if not os.path.exists(database):
    os.makedirs(os.path.dirname(database))
  f = open(database, "w+")
  f.close()

  call(["ruby", "src/gitlog.rb", database, "projects/" + PROJECT])
  return

conn = sqlite3.connect(DB)
cursor = conn.cursor()
cursor.execute("SELECT * FROM commits;")
commits = cursor.fetchall()

i = len(commits) - 1
n = 1
lastVersionHave = 0
while i > 0:
  i -= 50
  while (have_twohundred_commits(commits[i][Columns.SHA.value], lastVersionHave) == False):
    if i < 0:
      break
    print(i)
    i -= 1
  with cd("projects/" + PROJECT):
    call(["git", "checkout", commits[i][Columns.SHA.value]])
    lastVersionHave = int(check_output(["ruby", "./../../src/count-commits.rb", "./../../projects/" + PROJECT]))
  save_db(n)
  n += 1