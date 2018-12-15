# Channel Quality Control

**Input:** path to EEG .csv file

**Output:** channel list with scores
  * scores are a number betweeen 0-1 that indicate the proportion of the channel input that falls within an acceptable range
  * 1 indicates a properly functioning channel, 0 indicates no desired input is present (i.e. a bad channel)

**Language:**
  * Python 3.6

**Dependencies:**
  * pandas
  * SciPy
  * NumPy
