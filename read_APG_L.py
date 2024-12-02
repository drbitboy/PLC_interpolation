import os
import numpy as np

def read_table(combine=False):
  tables = list()
  for row in table_string.strip().split('\n'):
    ### Convert 'n.nn x 10 e'  to 'n.nnEe', which can be parsed by float
    munged = row.strip().replace('x 10','E').replace('<','').strip()
    if munged.startswith('https://'): continue
    try:
      value = float(munged.replace(' ',''))
      ### If valid float, append to table data values
      tables[-1][1].append(value)
    except:
      ### If no valid float, append to table column header names
      if not tables or tables[-1][1]:
        tables.append([list(),list()])
      tables[-1][0].append(row.strip())

  ### Ensure three columns of data are present
  assert not [1 for t in tables if (len(t[0]) % 3) or (len(t[1]) % 3)]

  ### Divide headers and table data values into three (key,data) pairs
  tables = [dict(zip(t[0][::int(len(t[0])/3)],np.array(t[1]).reshape((3,-1,))))
            for t in tables
           ]

  if combine:
    ### combine:  put all the tables into one table
    while len(tables) > 1:
      t = tables.pop()
      for k in t:
        tables[-1][k] = np.hstack((tables[-1][k],t[k],))
  else:
    ### not combine:  prepend the last entry in each table to the front
    ### of the next table
    for i in range(1,len(tables)):
      for k in tables[i]:
        tables[i][k] = np.hstack((tables[i-1][k][-1:],tables[i][k],))

  return tables

def binsearch_alternate(X, Xs,Ys):
  L = len(Xs)
  assert len(Ys) == L
  Z0,step,Lm1 = 0,64,L-1
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  step >>= 1; Z1 = Z0 + step; Z0 = (Z1 < Lm1 and X > Xs[Z1]) and Z1 or Z0
  Z1 = Z0 + 1
  return Ys[Z0] + ((X - Xs[Z0]) * (Ys[Z1] - Ys[Z0]) / (Xs[Z1] - Xs[Z0]))

def binsearch(X, Xs,Ys):
  L = len(Xs)
  assert len(Ys) == L
  if   X <   Xs[0]: lo,hi = 0,1
  elif X >= Xs[-1]: lo,hi = L-2,L-1
  else:
    lo,hi = 0,len(Xs)-1
    diff = hi
    while diff > 1:
      diff >>= 1
      mid = lo + diff
      if X > Xs[mid]: lo = mid
      else          : hi = mid
      diff = hi - lo
  return Ys[lo] + ((X - Xs[lo]) * (Ys[hi] - Ys[lo]) / (Xs[hi] - Xs[lo]))

def eighthundredone():
  table = read_table(combine=True).pop()
  Volts = [table[k] for k in table if '(V)' in k.upper()].pop()
  Ptorr = [table[k] for k in table if '(torr)' in k.lower()].pop()
  assert Volts[0] == 2.0 and Volts[-1] == 10.0
  assert Ptorr[0] == 7.5e-7 and Ptorr[-1] == 750.0
  for i in range(801):
    V = 2.0 + (i / 100.0)
    Y = binsearch(V,Volts,Ptorr)
    if not i: print('i,Volts,Ptorr')
    print(f'{i},{V:.2f},{Y:.3e}')

def test803():
  table = read_table(combine=True).pop()
  Volts = [table[k] for k in table if '(V)' in k.upper()].pop()
  Ptorr = [table[k] for k in table if '(torr)' in k.lower()].pop()
  assert Volts[0] == 2.0 and Volts[-1] == 10.0
  assert Ptorr[0] == 7.5e-7 and Ptorr[-1] == 750.0
  Vs = [2.0+((i-1)/100.0) for i in range(803)]
  A803 = np.array([binsearch          (V,Volts,Ptorr) for V in Vs])
  B803 = np.array([binsearch_alternate(V,Volts,Ptorr) for V in Vs])
  print(np.where(A803 != B803))
  print(np.vstack((A803,B803,)).T)

### Pasted from PDF on page at URL below
table_string = """
https://www.idealvac.com/files/brochures/Edwards_APG_MP_Manual.pdf#page=27
Pressure (mbar)
Druck (mbar)
Pression (mbar)
Output voltage (V)
Ausgangsspannung (V)
Tension de sortie (V)
Pressure (torr)
Druck (torr)
Pression (torr)
< 1 x 10-6
8.26 x 10 -5
2.27 x 10 -4
5.00 x 10 -4
1.08 x 10 -3
1.68 x 10 -3
2.60 x 10 -3
3.84 x 10 -3
5.15 x 10 -3
6.87 x 10 -3
1.05 x 10 -2
1.56 x 10 -2
2.10 x 10 -2
2.77 x 10 -2
3.45 x 10 -2
4.16 x 10 -2
5.04 x 10 -2
5.92 x 10 -2
8.74 x 10 -2
1.27 x 10 -1
1.71 x 10 -1
2.23 x 10 -1
2.90 x 10 -1
3.57 x 10 -1
2.00
2.05
2.10
2.20
2.40
2.60
2.80
3.00
3.20
3.40
3.60
3.80
4.00
4.20
4.40
4.60
4.80
5.00
5.20
5.40
5.60
5.80
6.00
6.20
< 7.5 x 10-7
6.20 x 10-5
1.70 x 10-4
3.75 x 10-4
8.10 x 10-4
1.26 x 10-3
1.95 x 10-3
2.88 x 10-3
3.86 x 10-3
5.15 x 10-3
7.88 x 10-3
1.17 x 10-2
1.58 x 10-2
2.08 x 10-2
2.59 x 10-2
3.12 x 10-2
3.78 x 10-2
4.44 x 10-2
6.56 x 10-2
9.53 x 10-2
1.28 x 10-1
1.67 x 10-1
2.18 x 10-1
2.68 x 10-1
Pressure (mbar)
Druck (mbar)
Pression (mbar)
Output voltage (V)
Ausgangsspannung (V)
Tension de sortie (V)
Pressure (torr)
Druck (torr)
Pression (torr)
4.35 x 10-1
5.33 x 10-1
6.40 x 10-1
7.67 x 10-1
9.23 x 10-1
1.14
1.40
1.66
1.92
2.38
2.95
3.51
4.17
5.40
7.06
9.69
1.29 x 10 1
1.66 x 10 1
2.07 x 10 1
3.39 x 10 1
6.32 x 10 1
1.44 x 10 2
1.00 x 10 3
6.40
6.60
6.80
7.00
7.20
7.40
7.60
7.80
8.00
8.20
8.40
8.60
8.80
9.00
9.20
9.40
9.50
9.60
9.70
9.80
9.90
9.95
10.00
3.26 x 10 -1
4.00 x 10 -1
4.80 x 10 -1
5.75 x 10 -1
6.92 x 10 -1
8.55 x 10 -1
1.05
1.25
1.44
1.79
2.21
2.63
3.13
4.05
5.30
7.27
9.68
1.24 x 10 1
1.55 x 10 1
2.54 x 10 1
4.74 x 10 1
1.08 x 10 2
7.50 x 10 2
"""
if "__main__" == __name__:
  t = read_table('ONETBL' in os.environ)
  print(t)
