'''
Description:

     A technique for detecting anomalies in seasonal univariate time
     series where the input is a series of <timestamp, count> pairs.


Usage:

     anomaly_detect_ts(x, max_anoms=0.1, direction="pos", alpha=0.05, only_last=None,
                      threshold="None", e_value=False, longterm=False, piecewise_median_period_weeks=2,
                      plot=False, y_log=False, xlabel="", ylabel="count", title=None, verbose=False)

Arguments:

       x: Time series as a two column data frame where the first column
          consists of the timestamps and the second column consists of
          the observations.

max_anoms: Maximum number of anomalies that S-H-ESD will detect as a
          percentage of the data.

direction: Directionality of the anomalies to be detected. Options are:
          "pos" | "neg" | "both".

   alpha: The level of statistical significance with which to accept or
          reject anomalies.

only_last: Find and report anomalies only within the last day or hr in
          the time series. None | "day" | "hr".

threshold: Only report positive going anoms above the threshold
          specified. Options are: None | "med_max" | "p95" |
          "p99".

 e_value: Add an additional column to the anoms output containing the
          expected value.

longterm: Increase anom detection efficacy for time series that are
         greater than a month. See Details below.

piecewise_median_period_weeks: The piecewise median time window as
          described in Vallis, Hochenbaum, and Kejariwal (2014).
          Defaults to 2.

    plot: A flag indicating if a plot with both the time series and the
          estimated anoms, indicated by circles, should also be
          returned.

   y_log: Apply log scaling to the y-axis. This helps with viewing
          plots that have extremely large positive anomalies relative
          to the rest of the data.

  xlabel: X-axis label to be added to the output plot.

  ylabel: Y-axis label to be added to the output plot.

   title: Title for the output plot.

 verbose: Enable debug messages
 
 resampling: whether ms or sec granularity should be resampled to min granularity. 
             Defaults to False.
             
 period_override: Override the auto-generated period
                  Defaults to None
                  
 multithreaded: whether to use multi-threaded implementation of DataFrame operations
                Defaults to False

Details:

     "longterm" This option should be set when the input time series
     is longer than a month. The option enables the approach described
     in Vallis, Hochenbaum, and Kejariwal (2014).
     "threshold" Filter all negative anomalies and those anomalies
     whose magnitude is smaller than one of the specified thresholds
     which include: the median of the daily max values (med_max), the
     95th percentile of the daily max values (p95), and the 99th
     percentile of the daily max values (p99).

Value:

    The returned value is a list with the following components.

    anoms: Data frame containing timestamps, values, and optionally
          expected values.

    plot: A graphical object if plotting was requested by the user. The
          plot contains the estimated anomalies annotated on the input
          time series.
     "threshold" Filter all negative anomalies and those anomalies
     whose magnitude is smaller than one of the specified thresholds
     which include: the median of the daily max values (med_max), the
     95th percentile of the daily max values (p95), and the 99th
     percentile of the daily max values (p99).

Value:

     The returned value is a list with the following components.

     anoms: Data frame containing timestamps, values, and optionally
          expected values.

     plot: A graphical object if plotting was requested by the user. The
          plot contains the estimated anomalies annotated on the input
          time series.
     One can save "anoms" to a file in the following fashion:
     write.csv(<return list name>[["anoms"]], file=<filename>)

     One can save "plot" to a file in the following fashion:
     ggsave(<filename>, plot=<return list name>[["plot"]])

References:

     Vallis, O., Hochenbaum, J. and Kejariwal, A., (2014) "A Novel
     Technique for Long-Term Anomaly Detection in the Cloud", 6th
     USENIX, Philadelphia, PA.

     Rosner, B., (May 1983), "Percentage Points for a Generalized ESD
     Many-Outlier Procedure" , Technometrics, 25(2), pp. 165-172.

See Also:

     anomaly_detect_vec

Examples:
     # To detect all anomalies
     anomaly_detect_ts(raw_data, max_anoms=0.02, direction="both", plot=True)
     # To detect only the anomalies in the last day, run the following:
     anomaly_detect_ts(raw_data, max_anoms=0.02, direction="both", only_last="day", plot=True)
     # To detect only the anomalies in the last hr, run the following:
     anomaly_detect_ts(raw_data, max_anoms=0.02, direction="both", only_last="hr", plot=True)
     # To detect only the anomalies in the last hr and resample data of ms or sec granularity:
     anomaly_detect_ts(raw_data, max_anoms=0.02, direction="both", only_last="hr", plot=True, resampling=True)
     # To detect anomalies in the last day specifying a period of 1440
     anomaly_detect_ts(raw_data, max_anoms=0.02, direction="both", only_last="hr", period_override=1440)

'''

import numpy as np
import scipy as sp
import pandas as pd
from multiprocessing import cpu_count
from dask import dataframe as ddf
from dask.dataframe import Series as ds

import datetime
import statsmodels.api as sm
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

'''
Raises ValueError with detailed error message if one of the two situations is true:
  1. calculated granularity is less than minute (sec or ms)
  2. resampling is not enabled for situations where calculated granularity < min
  
  level : string
    the granularity that is below the min threshold
    
'''
def _handle_granularity_error(level):
    e_message = '%s granularity is not supported. Ensure granularity => minute or enable resampling' % level
    raise ValueError(e_message)

'''
Resamples a data set to the min level of granularity

  data : Pandas or Dask Series
    input data set of (timestamp, float) in the form of a Series data structure
  period_override : int 
    indicates whether resampling should be done with overridden value instead of min (1440)
    
'''
def _resample_to_min(data, period_override=None):    
    data = data.resample('60s', label='right').sum()
    if _override_period(period_override):
        period = period_override
    else:
        period = 1440
    return (data, period)

'''
Indicates whether period can be overridden if the period derived from granularity does
not match the generated period.

  period_override : int
    the user-specified period that overrides the value calculated from granularity
'''
def _override_period(period_override):
        return period_override is not None

'''
Returns the generated period or overridden period depending upon the period_arg

  gran_period : int
    the period generated from the granularity
  period_arg : int
    the period to override the period generated from granularity
    
'''
def _get_period(gran_period, period_arg=None):
    if _override_period(period_arg):
        return period_arg
    else:
        return gran_period 

'''
Generates a tuple consisting of processed input data, a calculated or overridden period, and granularity

  raw_data : Pandas or Dask Series
    input data set of (timestamp, float) in the form of a Series data structure
  period_override : int
    period specified in the anomaly_detect_ts parameter list, None if it is not provided
  resampling : bool True | False
    indicates whether the raw_data should be resampled to a supporting granularity, if applicable
'''
def _get_data_tuple(raw_data, period_override, resampling=False):    
    data = raw_data.sort_index()
    timediff = _get_time_diff(data)
    
    if timediff.days > 0:
        period = _get_period(7, period_override)
        granularity = 'day'
    elif timediff.seconds / 60 / 60 >= 1:
        granularity = 'hr'
        period = _get_period(24, period_override)
    elif timediff.seconds / 60 >= 1:
        granularity = 'min'
        period = _get_period(1440, period_override)
    elif timediff.seconds > 0:
        granularity = 'sec'
        
        '''
           Aggregate data to minute level of granularity if data stream granularity is sec and
           resampling=True. If resampling=False, adjust period to sec level of granularity.
        '''      
        if resampling is True:
            data, period = _resample_to_min(data, period_override)
            granularity = 'min'
        else:
            period = _get_period(86400, period_override)
    else:
        '''
           Aggregate data to minute level of granularity if data stream granularity is ms and
           resampling=True. If resampling=False, raise ValueError
        '''
        if resampling is True:
            data, period = _resample_to_min(data, period_override)
            granularity = None
        else:
            _handle_granularity_error('ms')
    
    return (data, period, granularity)      

'''
Returns the time difference used to determine granularity and to generate the period

  data : Pandas or Dask Series
    input data set of (timestamp, float) in the form of a Series data structure
    
'''
def _get_time_diff(data):
    sub_series = data.head(2)
    return sub_series.index[1] - sub_series.index[0]

'''
Returns the max_anoms parameter used for S-H-ESD time series anomaly detection

  data : Pandas or Dask Series
    input data set of (timestamp, float) in the form of a Series data structure
  max_anoms : float
    the input max_anoms
    
'''
def _get_max_anoms(data, max_anoms):
    if max_anoms == 0:
        logging.warn('0 max_anoms results in max_outliers being 0.')
    return 1 / data.size if max_anoms < 1 / data.size else max_anoms

'''
Processes result set when longterm is set to true
  
  raw_data : Pandas or Dask Series
    input data set of (timestamp, float) in the form of a Series data structure
  a_series : AnomalySeries
    AnomalyDetection object encapsulating Pandas Series and optionally Dask Series objects
  period : int
    the calculated or overridden period value
  granularity : string
    the calculated or overridden granularity
  piecewise_median_period_weeks : int
    used to determine days and observations per period
  multithreaded : bool
    indicates if in single or multithreaded mode
    
'''    
def _process_long_term_data(raw_data, a_series, period, granularity, piecewise_median_period_weeks, multithreaded=False):
    # Pre-allocate list with size equal to the number of piecewise_median_period_weeks chunks in x + any left over chunk
    # handle edge cases for daily and single column data period lengths
    num_obs_in_period = period * piecewise_median_period_weeks + 1 if granularity == 'day' else period * 7 * piecewise_median_period_weeks
    num_days_in_period = (7 * piecewise_median_period_weeks) + 1 if granularity == 'day' else (7 * piecewise_median_period_weeks)
   
    all_data = []
        
    # Subset x into piecewise_median_period_weeks chunks
    for i in range(1, a_series.pandas_series.size + 1, num_obs_in_period):
        start_date = a_series.pandas_series.index[i]
        # if there is at least 14 days left, subset it, otherwise subset last_date - 14 days
        end_date = start_date + datetime.timedelta(days=num_days_in_period)
        
        if end_date < a_series.pandas_series.index[-1]:
            if multithreaded:
                boon = _execute_series_lambda_method(lambda data: data.loc[lambda raw_data: (raw_data.index >= start_date) & (raw_data.index <= end_date)], a_series.dask_series)
                all_data.append(_execute_series_lambda_method(lambda data: data.loc[lambda raw_data: (raw_data.index >= start_date) & (raw_data.index <= end_date)], a_series.dask_series))
            else:
                all_data.append(_execute_series_lambda_method(a_series.pandas_series.loc[lambda raw_data: (raw_data.index >= start_date) & (raw_data.index <= end_date)]))                
        else:
            if multithreaded:
                all_data.append(_execute_series_lambda_method(lambda data: data.loc[lambda raw_data: raw_data.index >= a_series.pandas_series.index[-1] - datetime.timedelta(days=num_days_in_period)], a_series.dask_series))
            else:
                all_data.append(_execute_series_lambda_method(a_series.pandas_series.loc[lambda raw_data: raw_data.index >= a_series.pandas_series.index[-1] - datetime.timedelta(days=num_days_in_period)]))                
    return all_data    

'''
Executes the function execution in multithreaded fashion by passing the function and 
Dask DataFrame to the Dask DataFrame.map_partitions function

  d_function : Function
    the lambda function to execute
  dask_series : Dask Series
    the Dask Series to compute the lambda function for
    
'''
def _execute_dask_lambda_method(d_function, dask_series):
    return dask_series.map_partitions(d_function).compute(scheduler='threads')

'''
Executes a function on a Pandas or Dask Series object

  d_function : Function
    the lambda function to execute
  dask_series_object : Dask Series 
    the Series to compute the lambda function for if in multithreaded mode
    
'''
def _execute_series_lambda_method(d_function, dask_series_object=None):
    if dask_series_object is not None:
        return _execute_dask_lambda_method(d_function, dask_series_object)
    else:
        return d_function

'''
Returns a Dask Series object from the Pandas Series object

  p_series : pandas.core.Series
    input data set of (timestamp, float) in the form of a Pandas Series data structure
    
'''
def _get_dask_series(p_series):
    return ddf.from_pandas(p_series, npartitions=cpu_count())

'''
Returns the results from the last day or hour only

  a_series : AnomalySeries
    AnomalyDetection object encapsulating Pandas Series and optionally Dask Series objects
  all_anoms : Series
    all of the timestamp-anomaly tuples returned by the algorithm
  granularity : string day | hr | min
    The supported granularity value
  only_last : string day | hr
    The subset of anomalies to be returned
  multithreaded : bool True | False
    indicates whether in standard or multithreaded mode
    
'''
def _get_only_last_results(a_series, all_anoms, granularity, only_last, multithreaded=False):
    start_date = a_series.pandas_series.index[-1] - datetime.timedelta(days=7)
    start_anoms = a_series.pandas_series.index[-1] - datetime.timedelta(days=1)

    if only_last == 'hr':
        # We need to change start_date and start_anoms for the hourly only_last option
        start_date = datetime.datetime.combine((a_series.pandas_series.index[-1] - datetime.timedelta(days=2)).date(), datetime.time.min)
        start_anoms = a_series.pandas_series.index[-1] - datetime.timedelta(hours=1)

    x_subset_single_day = None

    if multithreaded:
        anom_series = _get_dask_series(all_anoms)
    data = a_series.pandas_series

    # subset the last days worth of data
    if multithreaded:
        x_subset_single_day = _execute_series_lambda_method(lambda data: data.loc[data.index > start_anoms], a_series.dask_series)
    else:
        x_subset_single_day = _execute_series_lambda_method(a_series.pandas_series.loc[a_series.pandas_series.index > start_anoms])

    # When plotting anoms for the last day only we only show the previous weeks data
    if multithreaded:
        x_subset_week = _execute_series_lambda_method(lambda data: data.loc[lambda df: (df.index <= start_anoms) & (df.index > start_date)], a_series.dask_series)
    else:
        x_subset_week = _execute_series_lambda_method(data.loc[lambda df: (df.index <= start_anoms) & (df.index > start_date)])        

    if multithreaded:
        return _execute_series_lambda_method(lambda all_anoms: all_anoms.loc[all_anoms.index >= x_subset_single_day.index[0]], anom_series)
    else:        
        return _execute_series_lambda_method(all_anoms.loc[all_anoms.index >= x_subset_single_day.index[0]])

'''
Generates the breaks used in plotting

  granularity : string
    the supported granularity value
  only_last : True | False
    indicates whether only the last day or hour is returned and to be plotted
    
'''
def _get_plot_breaks(granularity, only_last):
    if granularity == 'day':
        breaks = 3 * 12
    elif only_last == 'day':
        breaks = 12
    else:
        breaks = 3
    return breaks

'''
Filters the list of anomalies per the threshold filter

  result_series : AnomalyResultSeries
    encapsulates the anoms returned by the algorithm in the form of Pandas Series and, optionally, Dask Series objects
  periodic_max : Pandas Series
    calculated daily max value
  threshold : str med_max | p95 | p99
    user-specified threshold value used to filter anoms
  multithreaded : bool True | False
    indicates whether in standard or multithreaded mode
    
'''
def _perform_threshold_filter(result_series, periodic_max, threshold, multithreaded=False):
    if threshold == 'med_max':
        # Dask Series does not support median() method, need to convert to Pandas Series
        if type(periodic_max) == ds:
            periodic_max = periodic_max.compute()
        thresh = periodic_max.median()
    elif threshold == 'p95':
        thresh = periodic_max.quantile(0.95)
    elif threshold == 'p99':
        thresh = periodic_max.quantile(0.99)
    else:
        raise AttributeError('Invalid threshold, threshold options are None | med_max | p95 | p99')

    if multithreaded:
        return _execute_series_lambda_method(lambda anoms: anoms.loc[anoms.values >= thresh], result_series.dask_series)
    else:
        return _execute_series_lambda_method(result_series.pandas_series.loc[result_series.pandas_series.values >= thresh]) 

'''
Calculates the max_outliers for an input data set

  a_series : Pandas Series
    Series object containing anomaly results
  max_percent_anomalies : float
    the input maximum number of anomalies per percent of data set values
    
'''
def _get_max_outliers(a_series, max_percent_anomalies):
    data_size = a_series.size
    max_outliers = int(np.trunc(data_size * max_percent_anomalies))
    assert max_outliers, 'With longterm=True, AnomalyDetection splits the data into 2 week periods by default. You have {0} observations in a period, which is too few. Set a higher piecewise_median_period_weeks.'.format(data_size)
    return max_outliers

'''
Returns a tuple consisting of two versions of the input data set: seasonally-decomposed and smoothed

  data : Pandas Series
    the input data set in the form of a Pandas Series data structure
  num_obs_per_period : int
    the number of observations in each period
    
'''
def _get_decomposed_data_tuple(data, num_obs_per_period):
    decomposed = sm.tsa.seasonal_decompose(data, freq=num_obs_per_period, two_sided=False)
    smoothed = data - decomposed.resid.fillna(0)
    data = data - decomposed.seasonal - data.mean()    
    return (data, smoothed)

'''
Returns an instance of the AnomalySeries container object
  pandas_series : Pandas Series
    the input Pandas Series object passed into the anomaly_detect_ts method
  multithreaded : bool
    the Dask Series object will be None if multithreaded=False
    
'''
def _get_anomaly_series(pandas_series, multithreaded=False):
    if multithreaded:
        return AnomalySeries(pandas_series, _get_dask_series(pandas_series))
    else:
        return AnomalySeries(pandas_series)

'''
Returns an instance of the AnomalyResultSeries container object
  pandas_series : Pandas Series
    the result Pandas Series object
  multithreaded : bool
    the Dask Series object will be None if multithreaded=False
    
'''
def _get_anomaly_result_series(pandas_series, multithreaded=False):
    if multithreaded:
        return AnomalySeries(pandas_series, _get_dask_series(pandas_series))
    else:
        return AnomalySeries(pandas_series)

'''
Calculates the periodic_max value used when threshold=True by resampling to ID granularity and finding max
  a_series : AnomalySeries
    the AnomalySeries object
  multithreaded : bool 
'''
def _calculate_periodic_max(a_series, multithreaded=False):
    if multithreaded:
        return a_series.dask_series.resample('1D').max()
    else:
        return a_series.pandas_series.resample('1D').max()

def anomaly_detect_ts(raw_data, max_anoms=0.1, direction="pos", alpha=0.05, only_last=None,
                      threshold=None, e_value=False, longterm=False, piecewise_median_period_weeks=2,
                      plot=False, y_log=False, xlabel="", ylabel="count", title='shesd output: ', verbose=False, 
                      dropna=False, resampling=False, period_override=None, multithreaded=False):

    if verbose:
        logging.info("Validating input parameters")
    # validation
    assert isinstance(raw_data, pd.Series) or isinstance(raw_data,ddf.Series), 'Data must be a Pandas or Dask Series'
    assert raw_data.values.dtype in [int, float], 'Values of the series must be number'
    assert raw_data.index.dtype == np.dtype('datetime64[ns]'), 'Index of the series must be datetime'
    assert max_anoms <= 0.49 and max_anoms >= 0, 'max_anoms must be non-negative and less than 50% '
    assert direction in ['pos', 'neg', 'both'], 'direction options: pos | neg | both'
    assert only_last in [None, 'day', 'hr'], 'only_last options: None | day | hr'
    assert threshold in [None, 'med_max', 'p95', 'p99'], 'threshold options: None | med_max | p95 | p99'
    assert piecewise_median_period_weeks >= 2, 'piecewise_median_period_weeks must be greater than 2 weeks'  
    if verbose:
        logging.info('Completed validation of input parameters')
        
    if alpha < 0.01 or alpha > 0.1:
        logging.warn('alpha is the statistical significance and is usually between 0.01 and 0.1')
    
    # TODO Allow raw_data.index to be number, here we can convert it to datetime

    data, period, granularity = _get_data_tuple(raw_data, period_override, resampling)
    
    a_series = _get_anomaly_series(data, multithreaded)
    
    if granularity is 'day':
        num_days_per_line = 7
        # TODO determine why this is here
        only_last = 'day' if only_last == 'hr' else only_last

    max_anoms = _get_max_anoms(data, max_anoms)
 
    # If longterm is enabled, break the data into subset data frames and store in all_data
    if longterm:
        all_data = _process_long_term_data(raw_data, a_series, period, granularity, piecewise_median_period_weeks, multithreaded)
    else:
        all_data = [data]

    all_anoms = pd.Series()
    seasonal_plus_trend = pd.Series()
    
    # Detect anomalies on all data (either entire data in one-pass, or in 2 week blocks if longterm=True)
    for series in all_data:
        shesd = _detect_anoms(series, k=max_anoms, alpha=alpha, num_obs_per_period=period, use_decomp=True, 
                              use_esd=False, direction=direction, verbose=verbose, multithreaded=multithreaded)
        shesd_anoms = shesd['anoms']
        shesd_stl = shesd['stl']

        # -- Step 3: Use detected anomaly timestamps to extract the actual anomalies (timestamp and value) from the data
        anoms = pd.Series() if shesd_anoms.empty else series.loc[shesd_anoms.index]
    
        result_series = _get_anomaly_result_series(anoms, multithreaded)
        
        # Filter the anomalies using one of the thresholding functions if applicable
        if threshold:
            # Calculate daily max values
            periodic_max = _calculate_periodic_max(a_series, multithreaded)
            
            anoms = _perform_threshold_filter(result_series, periodic_max, threshold, multithreaded)

        all_anoms = all_anoms.append(anoms)
        seasonal_plus_trend = seasonal_plus_trend.append(shesd_stl)

    # De-dupe 
    all_anoms.drop_duplicates(inplace=True)
    seasonal_plus_trend.drop_duplicates(inplace=True)

    # If only_last is specified, create a subset of the data corresponding to the most recent day or hour
    if only_last:
        all_anoms = _get_only_last_results(a_series, all_anoms, granularity, only_last, multithreaded)
 
    # If there are no anoms, log it and return an empty anoms result
    if all_anoms.empty:
        if verbose:
            logging.info('No anomalies detected.')

        return {
            'anoms': pd.Series(),
            'plot': None
        }

    if plot:
        #TODO additional refactoring and logic needed to support plotting
        num_days_per_line
        #breaks = _get_plot_breaks(granularity, only_last)
        #x_subset_week
        raise Exception('TODO: Unsupported now')

    return {
        'anoms': all_anoms,
        'expected': seasonal_plus_trend if e_value else None,
        'plot': 'TODO' if plot else None
    }

# Detects anomalies in a time series using S-H-ESD.
#
# Args:
#	 a_series: Pandas Series containing input values 
#	 k: Maximum number of anomalies that S-H-ESD will detect as a percentage of the data.
#	 alpha: The level of statistical significance with which to accept or reject anomalies.
#	 num_obs_per_period: Defines the number of observations in a single period, and used during seasonal decomposition.
#	 use_decomp: Use seasonal decomposition during anomaly detection.
#	 use_esd: Uses regular ESD instead of hybrid-ESD. Note hybrid-ESD is more statistically robust.
#	 one_tail: If TRUE only positive or negative going anomalies are detected depending on if upper_tail is TRUE or FALSE.
#	 upper_tail: If TRUE and one_tail is also TRUE, detect only positive going (right-tailed) anomalies. If FALSE and one_tail is TRUE, only detect negative (left-tailed) anomalies.
#	 verbose: Additionally printing for debugging.
#    multithreaded: indicates if in single or multithreaded mode
# Returns:
#   A list containing the anomalies (anoms) and decomposition components (stl).

def _detect_anoms(a_series, k=0.49, alpha=0.05, num_obs_per_period=None,
                  use_decomp=True, use_esd=False, direction="pos", verbose=False, multithreaded=False):

    # validation
    assert num_obs_per_period, "must supply period length for time series decomposition"
    assert direction in ['pos', 'neg', 'both'], 'direction options: pos | neg | both'
    assert a_series.size >= num_obs_per_period * 2, 'Anomaly detection needs at least 2 periods worth of data'
    assert a_series[a_series.isnull()].empty, 'Data contains NA. We suggest replacing NA with interpolated values before detecting anomaly'

    # conversion
    one_tail = True if direction in ['pos', 'neg'] else False
    upper_tail = True if direction in ['pos', 'both'] else False

    # -- Step 1: Decompose data. This returns a univariate remainder which will be used for anomaly detection. Optionally, we might NOT decompose.
    # Note: R use stl, but here we will use MA, the result may be different TODO.. Here need improvement
    #decomposed = sm.tsa.seasonal_decompose(data, freq=num_obs_per_period, two_sided=False)
    #smoothed = data - decomposed.resid.fillna(0)
    #data = data - decomposed.seasonal - data.mean()

    data, smoothed = _get_decomposed_data_tuple(a_series, num_obs_per_period)
    
    # Update the max_outliers parameter
    max_outliers = _get_max_outliers(data, k)

    R_idx = pd.Series()

    #n = data.size
    n = data.size
    
    # Compute test statistic until r=max_outliers values have been
    # removed from the sample.
    for i in range(1, max_outliers + 1):
        if verbose:
            logging.info(i, '/', max_outliers, ' completed')

        if not data.mad():
            break

        if not one_tail:
            ares = abs(data - data.median())
        elif upper_tail:
            ares = data - data.median()
        else:
            ares = data.median() - data

        ares = ares / data.mad()

        tmp_anom_index = ares[ares.values == ares.max()].index
        cand = pd.Series(data.loc[tmp_anom_index], index=tmp_anom_index)

        data.drop(tmp_anom_index, inplace=True)

        # Compute critical value.
        p = 1 - alpha / (n - i + 1) if one_tail else (1 - alpha / (2 * (n - i + 1)))
        t = sp.stats.t.ppf(p, n - i - 1)
        lam = t * (n - i) / np.sqrt((n - i - 1 + t ** 2) * (n - i + 1))
        if ares.max() > lam:
            R_idx = R_idx.append(cand)

    return {
        'anoms': R_idx,
        'stl': smoothed
    }

'''
Encapsulates Pandas Series and, if multithreaded enabled, a Dask Series 
representations of the input data

'''
class AnomalySeries():
    def __init__(self, pandas_series, dask_series=None):
        self.pandas_series = pandas_series
        self.dask_series = dask_series
    
    '''
    Indicates whether in multithreaded mode, meaning that the dask_series
    instance attribute is not None
    
    '''
    def multithreaded_enabled(self):
        return self.dask_series is not None
    
    '''
    Returns the size of the encapsulated Series object, either Pandas (single threaded)
    or Dask (multithreaded mode)
    
    '''
    def size(self):
        if self.multithreaded_enabled():
            return self.dask_series.size.compute()
        else:
            return self.pandas_series.size

'''
Encapsulates Pandas Series and, if multithreaded enabled, a Dask Series 
representations of the input data

'''
class AnomalyResultSeries():
    def __init__(self, pandas_series, dask_series=None):
        self.pandas_series = pandas_series
        self.dask_series = dask_series                      