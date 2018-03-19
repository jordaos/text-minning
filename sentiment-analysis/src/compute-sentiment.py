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

PATH = '../minning-util-codes/DBs/' + PROJECT + '/parts'

folders = next(os.walk(PATH))[1]

for i in range(len(folders)):
  i += 1
  file_commits = "%s/%i_part/%i_part-all.txt" % (PATH, i, i)
  with cd("data/sentistrength"):
    call(["java", "-jar", "sentistrength-0.1.jar", "sentidata", "sentistrength_data/", "input", "../../%s" % file_commits, "explain"])