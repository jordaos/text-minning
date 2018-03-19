import sqlite3
import sys
import os
import math
import csv

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

csvfile = '../minning-util-codes/DBs/' + PROJECT + '/' + PROJECT + '.csv'

with open(csvfile, 'w') as csvfile:
  fieldnames = ['part', 'neg', 'neu', 'pos']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for i in range(len(folders)):
    i += 1

    dir = "%s/%i_part/txt_ss" % (PATH, i)
    if not os.path.exists(dir):
      os.makedirs(dir)
      os.makedirs("%s/pos" % dir)
      os.makedirs("%s/neg" % dir)
      os.makedirs("%s/neu" % dir)

    database = "%s/%i_part/%i_part.sqlite" % (PATH, i, i)
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sentiment;")
    commits = cursor.fetchall()

    qtd_pos = 0
    qtd_neg = 0
    qtd_neu = 0

    for linha in commits:
      message = linha[4]
      sha = linha[1]
      pos = math.fabs(linha[2])
      neg = math.fabs(linha[3])

      if pos == neg:
        qtd_neu += 1
        with open("%s/neu/%s.txt" % (dir, sha), "a") as arq:
          arq.write(message)
          arq.close()
      elif pos > neg:
        qtd_pos += 1
        with open("%s/pos/%s.txt" % (dir, sha), "a") as arq:
          arq.write(message)
          arq.close()
      else:
        qtd_neg += 1
        with open("%s/neg/%s.txt" % (dir, sha), "a") as arq:
          arq.write(message)
          arq.close()

    writer.writerow({'part': '%i_part' % i, 'neg': qtd_neg, 'neu': qtd_neu, 'pos': qtd_pos})
