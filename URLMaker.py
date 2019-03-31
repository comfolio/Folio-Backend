import datetime
import calendar

current_time = datetime.datetime.now(datetime.timezone.utc)
defaultstartdate = int(current_time.timestamp() - (360 * 24 * 60 * 60 * 5))
def URLMaker(dictionary, startdate = defaultstartdate):
    """URLMaker is a function that takes a dictionary input in {Ticker:Value,...} format
    and the start date formatted in epoch time and returns the Blackrock API URL Call."""
    ##dictionary is the inputted dictionary in {ticker:percent ,...} format
    ##startdate is the startdate in epoch time.
    #Creating base URL string for call.
    URL = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&graph=resultMap.PORTFOLIOS%5Bportfolios%5Breturns%5BperformanceChart%5D%5D%5D&identifierType=ticker&positions="
    count = 1
    for key,value in dictionary.items():
        URL += key + "~" + str(value)
        if len(dictionary.items()) != count:
            URL += "%7C"
        count += 1
    URL += "&startDate=" + str(startdate)
    return(URL)
    """#Initializing separate URL variables.
    current_time = datetime.datetime.now(datetime.timezone.utc)"""
    

    #Not utilized: Portfolio performance across time.
    """ URL5Y = URL + str(int(current_time.timestamp() - (365 * 24 * 60 * 60 * 5)))
    URL1Y = URL + str(int(current_time.timestamp() - (365 * 24 * 60 * 60)))
    URL6M = URL + str(int(current_time.timestamp() - (182.5 * 24 * 60 * 60 )))
    URL3M = URL + str(int(current_time.timestamp() - (91.25 * 24 * 60 * 60)))
    URL1M = URL + str(int(current_time.timestamp() - (30.4125 * 24 * 60 * 60))) """
    #return URL5Y, URL1Y, URL6M, URL3M, URL1M  

#URLMaker({"AAPL":50, "NFLX":25, "FB":20, "MSFT":5}, int(datetime.datetime.now(datetime.timezone.utc).timestamp() - (365 * 24 * 60 * 60)))

def URLMakerExposure(dictionary):
    URL = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&graph=resultMap.PORTFOLIOS%5Bportfolios%5Bexposures%5BassetClass%5D%5D%5D&identifierType=ticker&includeAllBreakdowns=true&positions="
    count = 1
    for key,value in dictionary.items():
        URL += key + "~" + str(value)
        if len(dictionary.items()) != count:
            URL += "%7C"
        count += 1
    return URL

print(URLMakerExposure({"MSFT":50, "NFLX":20, "FB":20, "AMZN":10}))