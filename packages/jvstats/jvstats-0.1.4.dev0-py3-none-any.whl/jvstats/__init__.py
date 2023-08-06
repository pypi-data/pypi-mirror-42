from statistics import median

class Delays:

  def __init__(self, delays=[],width=3):

    #initializes the  median
    self.__medians=[]

    #sets the initial width of the sliding window
    self.width = width

    # sets the initial list of delays
    self.delays = delays

    # sets the initial sliding window
    self.__sliding_window = self.getSlidingWindow(delays,width,len(delays))

  @property
  def delays(self):
    return self.__delays

  @property
  def width(self):
    return self.__width

  @property
  def sliding_window(self):
    return self.__sliding_window

  @property
  def medians(self):
    return self.__medians

  @delays.setter
  def delays(self, dls):

    # check that the delays set is either an integer or a list of integers
    if isinstance(dls,int):
      self.__delays = [dls]
      self.recalculateMedians()
    elif all(isinstance(x,int) for x in dls):
      self.__delays = dls
      self.recalculateMedians()
    else:
      raise TypeError("delays must either be integer or an array of integers")


  @width.setter
  def width(self,wdh):
    if isinstance(wdh,int):
      self.__width=wdh
    else:
      self.__width=None
      raise TypeError("width must be an integer")
  
  def addDelay(self,delay):
    '''
    Adds a delay value to the list of delays

    Parameters:
    delay (int,Array): the delay to add to the list of delays
 
    Returns:
    Array: The list of delays
    '''

    # check that the delay added is either an integer or list of integers
    if isinstance(delay,int):
      self.__delays.append(delay)

      # we added a delay so let's slide the window and append the  median
      self.updateSlidingWindow()
      self.appendMedian()

    elif all(isinstance(x,int) for x in delay):
      self.__delays+=delay

      # since we are appending a whole bunch of delays
      # we slide the window and recalculate the median
      self.recalculateMedians()
    else:
      raise TypeError("delay must be an integer or array of integers")


    return self.__delays

  def get_Median(self):
    return self.medians

  def updateSlidingWindow(self):
    # set the new sliding window for stats
    self.__sliding_window = self.getSlidingWindow(self.__delays,self.width,0)

  @staticmethod
  def getSlidingWindow(delays=[],width=3,offset=0):
    if (len(delays) < width):
      return delays
    else:
      return delays[len(delays)-width:len(delays)]

  # From here on out are stats to measure for

  # MEDIAN
  def appendMedian(self):
    # This function adds a median dependent on the current window to check
    # this is useful for when we iteratively add delay values
    if len(self.sliding_window)==1:
      self.__medians.append(-1)
    else:
      self.__medians.append(int(median(self.sliding_window)))

  def recalculateMedians(self):

    # we make a copy of the current delays and zero it
    delays = self.delays.copy()
    self.__delays=[]
    self.__medians=[]
    for delay in delays:
      self.addDelay(delay)

