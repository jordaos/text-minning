import sqlite3
import sys
import os
import re

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
  conn.text_factory = str
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM commits;")
  commits = cursor.fetchall()
  cursor.execute('''CREATE TABLE IF NOT EXISTS `sentiment` 
                    ( `project` TEXT, 
                    `sha` TEXT, 
                    `Positive` INTEGER, 
                    `Negative` INTEGER, 
                    `Text` TEXT, 
                    `Explanation` TEXT )''')
  
  file_name = "%i_part-all0_out.txt" % (i)
  file = open("%s/%i_part/%s" % (PATH, i, file_name), "r")
  commit_analysis = file.readline()

  for linha in commits:
    commit_analysis = file.readline()
    arr_analysis = re.split(r'\t+', commit_analysis)
    cursor.execute("""
        INSERT INTO sentiment (project, sha, Positive, Negative, Text, Explanation)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (linha[0], linha[1], arr_analysis[0], arr_analysis[1], linha[2], arr_analysis[3]))
  file.close()
  conn.commit()
  conn.close()