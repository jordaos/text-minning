import sqlite3
import sys
import os

# encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

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

  database = "%s/%i_part/%i_part.sqlite" % (PATH, i, i)
  conn = sqlite3.connect(database)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM commits;")
  commits = cursor.fetchall()
  
  file_name = "%s_part-all.txt" % (i)
  file = open("%s/%i_part/%s" % (PATH, i, file_name), "w")

  for linha in commits:
    file.write(linha[2].replace('\n', ' ') + '\n')
  file.close()
  conn.close()