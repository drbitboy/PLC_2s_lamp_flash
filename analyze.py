import re
import os
import sys
import numpy
import matplotlib.pyplot as plt

class STATS(object):
  """Class to parse RSLogix [Print Report ...] data"""

  ### PDF from RSLogix [Print Report ...] option, converted to
  ### single-file HTML by LibreOffice Draw [Export ...] option, contains
  ### lines similar to the following, which contain the delta-times
  ### between toggling of the lamp output, in integer units of 100us,
  ### per MicroLogix 1100 free-running clock.
  ###
  ### <p>N9:0      17685  20008  19999  19998  20004  20000  20000  19997  20009  20003 </p>
  ###              |<-------------------------data----------------------------------->|
  ###              |                                                                  |
  ###    prefix<---|                                                                  |--->suffix
  ###
  ### Here is a regular expression method to match lines like those
  ###
  matchn9 = re.compile("^<p>N9:\d+\s+([^\s].*\d)\s*</p>\s*$").match
  ###                                |<-data-->|
  ###                                |         |
  ###                      <---prefix|         |suffix--->

  def __init__(self,html_filename):
    """Initializer parses HTML data, converts to numpy.ndarray"""

    self.fn = html_filename
    self.bn = os.path.basename(self.fn)

    with open(html_filename,'r') as f_html_input:
      self.data = numpy.array(
        [val
         for val in sum([list(map(float,match.groups()[0].split()))
                         for match in map(STATS.matchn9,f_html_input)
                         if not (match is None)
                        ]
                       ,[]
                       )[1:]
         if val>1e4
        ]
      )
    self.L = self.data.size

  def mean(self):
    """Return mean of data"""
    return self.data.mean()

  def std(self):
    """Return standard deviation of data"""
    return self.data.std()

  def lucls(self,factor=3.0):
    """Return pseudo-LCL and - UCL, (factor*std) offset from mean"""
    fs,m = factor*self.std(),self.mean()
    return m-fs,m+fs,factor

  def plotlims(self,factor=3.0):
    """Plot data in LCL/UCL-ish form"""
    lcl,ucl,factor = self.lucls(factor=factor)
    plt.axhline(ucl,color='g',label='UCL')
    plt.axhline(lcl,color='b',label='LCL')
    plt.axhline(self.mean(),color='r',linestyle='dotted',label='Mean')
    plt.plot(self.data,'ko-',label='Data')
    plt.legend()
    plt.ylabel('On-off and Off-on time, 100us (1e-4s) intervals')
    plt.xlabel('Sample #')
    plt.title('{0}\nMean={1:.3f}; Stddev={2:.3f}; CLfactor={3:.1f}'
              .format(self.bn
                     ,self.mean()
                     ,self.std()
                     ,float(factor)
                     )
              )
    plt.show()

  def plotcumfreq(self):
    """Plot data cumulative frequency distribution"""
    plt.axhline(self.L/2.0,color='r',linestyle='dotted',label='Median')
    plt.axvline(self.mean(),color='r',linestyle='dotted',label='Mean')
    plt.plot(numpy.sort(self.data),numpy.arange(self.L)+1,'kx-',label='Sorted data')
    plt.legend()
    plt.ylabel('# of samples less than or equal to times')
    plt.xlabel('Sorted On-off and Off-on times, 100us (1e-4s) intervals')
    plt.title('{0}\nMean={1:.3f}; Stddev={2:.3f}'
              .format(self.bn
                     ,self.mean()
                     ,self.std()
                     )
              )
    plt.show()

  def plotfreq(self):
    """Plot data frequency distribution"""
    plt.axvline(self.mean(),color='r',linestyle='dotted',label='Mean')
    mn,mx = self.data.min(),self.data.max()
    freqs,times = numpy.histogram(self.data
                                 ,bins=int(1+mx-mn)
                                 ,range=(mn-.5,mx+.5,)
                                 )
    plt.bar(times[:-1]+0.5,freqs,label='Histogram')
    plt.legend()
    plt.ylabel('# of samples at time')
    plt.xlabel('On-off and Off-on times, 100us (1e-4s) intervals')
    plt.title('{0}\nMean={1:.3f}; Stddev={2:.3f}'
              .format(self.bn
                     ,self.mean()
                     ,self.std()
                     )
              )
    plt.show()


########################################################################
if "__main__" == __name__:
  dt = dict()
  for arg in sys.argv[1:]:
    if '--doplot'==arg: continue
    dt[arg] = STATS(arg)

  for fn in dt:
    dt[fn].plotlims()
    dt[fn].plotcumfreq()
    dt[fn].plotfreq()
