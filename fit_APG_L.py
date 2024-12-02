import os
import sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

### Model for method curve_fit is polynomial
def model(x,*p):
    return np.polyval(p,x)

def go(table,order,chop):
  """
Fit Voltage vs. log10(Pressure in Torr) to polyomial of given order
- table:  newline-seperated string data
- order:  order of polynomial fit; there will be order+1 coefficients
- chop:  [left,right] number of endpoints to ignore
"""

  ### Get data as Pandas DataFrame; index is Voltage
  df = table2df(table) 

  ### Extract data to Numpy arrays; use pressures in Torr
  xdata = df.index.to_numpy()
  ydata = np.log10(df.Ptorr.to_numpy())

  ### Initialize polynomial coefficients
  ### Estimate linear slope of central data
  p0 = np.zeros(order+1)
  p0[-2] = ((ydata[1+chop[0]:] - ydata[:-1-chop[1]]) / (xdata[1+chop[0]:]-xdata[:-1-chop[1]])).mean()

  ### Perform fit
  popt,pcov = curve_fit(model, xdata[chop[0]:len(xdata)-chop[1]], ydata[chop[0]:len(xdata)-chop[1]], p0)
  print(popt)

  ### Plot results
  import matplotlib.pyplot as plt
  plt.plot(xdata,df.Ptorr,'-x',label='Ptorr')
  plt.plot(xdata,10.0**model(xdata,*popt),'o',label='Fit')
  plt.xlabel('Voltage, V')
  plt.ylabel('P, mbar or torr')
  plt.title(f'Order = {order}; Chops = {chop}')
  if not ('GOLINEAR' in os.environ): plt.semilogy()
  plt.legend()
  plt.show()

def table2df(table):
  """
Parse table data
   
Three columns of data look like this:

Pmbar
1 x 10-6       <== start of pressure data in units of mbar
8.26 x 10 -5
...
Volt
2.00           <== start of volage data
2.05
...
Ptorr
7.5 x 10-7     <== start of pressure data in units of torr
6.20 x 10-5
...

"""

  ### Dictionary of the three columns
  coldict = dict()

  ### Parse data from lines (rows) in table
  for row in table.strip().split('\n'):
    try:
      ### '1.23 x 10 -1' => float('1.23E-1')
      ### '2.31 x 10-1'  => float('2.31E-1')
      ### '2.31 x 103'   => float('2.31E3')
      ### etc.
      value = float(row.strip().replace("x 10","E").replace(" ",""))
    except:
      ### If float throws exception, row = name of following column data
      ### - Save name of current column
      ### - Initialize current column as empty list
      ### - Skip to next row (line) of data
      columnname = row.strip().replace(' ','')
      coldict[columnname] = []
      continue

    ### Add value to current 
    coldict[columnname].append(value)

  index = coldict['Volt']
  del coldict['Volt']
  return pd.DataFrame(coldict,index=index)

### Table from https://www.idealvac.com/files/brochures/Edwards_APG_MP_Manual.pdf#page=27
tabledata = """
Pmbar
1 x 10-6
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
Volt
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
Ptorr
7.5 x 10-7
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
  go(tabledata
    ,sys.argv[1:] and int(sys.argv[1]) or 5
    ,[int(s) for s in sys.argv[2:]+[0,0]][:2]
    )
