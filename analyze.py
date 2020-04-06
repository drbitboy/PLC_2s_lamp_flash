import re
import os
import sys
import numpy
import matplotlib.pyplot as plt

class STATS(object):
  def __init__(self,lt):
    self.data = numpy.array(lt)
    self.L = len(lt)
  def mean(self): return self.data.mean()
  def std(self): return self.data.std()
  def lucls(self,factor=3.0):
    fs,m = factor*self.std(),self.mean()
    return m-fs,m+fs,factor

### <p>N9:0      17685  20008  19999  19998  20004  20000  20000  19997  20009  20003 </p>
matchn9 = re.compile("^<p>N9:\d+ (.*)</p>\s*$").match
if "__main__" == __name__:
  dt = dict()
  for arg in sys.argv[1:]:
    if '--doplot'==arg: continue
    with open(arg,'r') as f_html_input:
      dt[arg] = STATS(
        [val
         for val in sum([list(map(float,match.groups()[0].split()))
                         for match in map(matchn9,f_html_input)
                         if not (match is None)
                        ]
                       ,[]
                       )[1:]
         if val>1e4
        ]
      )

  for fn in dt:
    stats = dt[fn]
    lcl,ucl,factor = stats.lucls()
    plt.axhline(ucl,color='g',label='UCL')
    plt.axhline(lcl,color='b',label='LCL')
    plt.axhline(stats.mean(),color='r',linestyle='dotted',label='Mean')
    plt.plot(stats.data,'ko-',label='Data')
    plt.legend()
    plt.ylabel('On-off and Off-on time, 100us (1e-4s) intervals')
    plt.xlabel('Sample #')
    plt.title('{0}\nMean={1:.3f}; Stddev={2:.3f}; CLfactor={3:.1f}'
              .format(os.path.basename(fn)
                     ,stats.mean()
                     ,stats.std()
                     ,float(factor)
                     )
              )
    plt.show()
