# Table of Contents

1.  [HFFE: High-Frequency Financial Econometrics](#orgf11f455)
    1.  [Introduction](#org97eed1c)
    2.  [Stocks](#org33c56cd)
    3.  [Options](#orgf5f80a1)
    4.  [Under development](#orgcbddafb)
	1.  [Redo introduction](#org9c56278)
	2.  [Add examples on how to use stock.py](#org854d2d5)
	3.  [Add examples on how to use options.py](#org8640d8b)
	4.  [Change file stock.py to stocks.py](#org5f4afbb)
	5.  [Add citations](#orge52187d)
	6.  [Sample data](#org17953b9)
	7.  [[stock.py] Change internals to pandas dataframe](#org3773095)
	8.  [[stock.py]](#orgf3f595f)
	9.  [[stock.py] Truncated variance estimator](#org116e719)
	10. [[stock.py] Local volatility estimator](#org505785b)
	11. [[stock.py] Confidence intervals](#org7494949)


<a id="orgf11f455"></a>

# HFFE: High-Frequency Financial Econometrics


<a id="org97eed1c"></a>

## Introduction

This package implements some tools of the high-frequency financial econometrics literature.
The HFFE package provides a class `Stock`. This class can be used in two ways:

1.  Instantiate the class and provide stock data. The instance `__init__` method will automatically compute geometric returns, realized and bipower variances, and separate diffusive from jump returns using the stock data supplied.
2.  Use the class methods by themselves as needed. All of the methods in `Stock` are static methods and can be used without instantiating the class.

The class can be instantiated via the default constructor by supplying an iterable containing prices (floats) and an iterable containing date stamps (in the format YYYYMMDD for year, month and day). The default constructor also takes an optional iterable containing time stamps (in the format HHMM for hour and minute or HHMMSS for hour, minute and second).
The data is assumed to be rectangular, meaning that each day contains the same number of price observations.

Prices are assumed to be observed \(N\) times per day, at the same discrete intervals. For example, if prices are sampled every 5 minutes starting from 9:30 AM and finishing at 4:00 PM, then we will have \(N=79\) price observations per day.
Prices are assumed to be observed for \(T\) total days. In each of these \(T\) days we have \(N\) price observations.
Geometric returns (log-returns) are computed for each of the days and for each of the discrete sampling intervals. However, <span class="underline">overnight returns are not considered, and the packaged only focuses on the analysis of intraday returns.</span>
If there are \(N=79\) price observations each day, then we will have \(n=78\) returns each day.

Example:

    from hffe import Stock
    from random import normalvariate as randn
    # generate some fake data
    prices = np.array([10.0 + randn(0, 1) for _ in range(10)])
    dates = ['20181112']*len(prices)
    times = [f'093{i}' for i in range(10)]
    # instantiate class
    stock = Stock(prices, dates, times)
    # at this point we can access the returns, variance measures and
    # obtain the diffusive returns separated from the jump returns
    print(f'Number of prices per day: {stock.total["prices"]}\n'
	  f'Number of days: {stock.total["days"]}')
    print(stock.returns)
    # print measures of variance
    print(f'Realized Variance: {stock.RV}\n'
	  f'Annualized Realized Variance: {(252*stock.RV)**0.5}\n'
	  f'Bipower Variance: {stock.BV}\n'
	  f'Annualized Bipower Variance: {(252*stock.BV)**0.5}')


<a id="org33c56cd"></a>

## Stocks


<a id="orgf5f80a1"></a>

## Options


<a id="orgcbddafb"></a>

## Under development


<a id="org9c56278"></a>

### TODO Redo introduction


<a id="org854d2d5"></a>

### TODO Add examples on how to use stock.py


<a id="org8640d8b"></a>

### TODO Add examples on how to use options.py


<a id="org5f4afbb"></a>

### TODO Change file stock.py to stocks.py


<a id="orge52187d"></a>

### TODO Add citations

1.  TODO To volatility estimators

2.  TODO To jump threshold and separtion

3.  TODO To time-of-day factor


<a id="org17953b9"></a>

### TODO Sample data

1.  TODO Sample stock data

2.  TODO Sample SPX options data


<a id="org3773095"></a>

### TODO [stock.py] Change internals to pandas dataframe


<a id="orgf3f595f"></a>

### TODO [stock.py]


<a id="org116e719"></a>

### TODO [stock.py] Truncated variance estimator


<a id="org505785b"></a>

### TODO [stock.py] Local volatility estimator


<a id="org7494949"></a>

### TODO [stock.py] Confidence intervals
