import sqlite3
import sys
import os

PROJECT = ''
if len(sys.argv) > 1:
  PROJECT = sys.argv[1]
else:
  print 'Give parameter (project name)'
  sys.exit()

PATH = 'DBs/' + PROJECT + '/parts'

folders = next(os.walk(PATH))[1]

for i in reversed(range(len(folders))):
  if (i == 0):
    break
  i += 1

  connAt = sqlite3.connect('%s/%d_part/%d_part.sqlite' % (PATH, i, i)) # At = atual
  connAt.row_factory = lambda cursor, row: row[0]
  cursorAt = connAt.cursor()

  connAnt = sqlite3.connect('%s/%d_part/%d_part.sqlite' % (PATH, i - 1, i - 1)) # Ant = anterior
  connAnt.row_factory = lambda cursor, row: row[0]
  cursorAnt = connAnt.cursor()
  listCommitsAnt = cursorAnt.execute('SELECT sha FROM commits;').fetchall()
  qtdAntBefore = len(listCommitsAnt)

  cursorAt.execute("SELECT sha FROM commits")
  qtdAtBefore = 0

  for sha in cursorAt.fetchall():
      qtdAtBefore += 1
      if sha in listCommitsAnt:
          cursorAt.execute("""
              DELETE FROM commits 
              WHERE sha = ?""", (sha,))
  connAt.commit()

  cursorAt.execute("""
      SELECT sha FROM commits
  """)
  qtdAtAfter = len(cursorAt.fetchall())
  
  connAt.close()
  connAnt.close()

  print('=========Parte %d=========' % (i))
  print('Tinha %d' % (qtdAtBefore))
  print('Anterior(%d_part) tem %d' % (i - 1, qtdAntBefore))
  print('Atual deveria ter %d' % (qtdAtBefore - qtdAntBefore))
  print('Tem %d' % (qtdAtAfter))