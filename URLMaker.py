import datetime
import calendar


def URLMaker(dictionary):
    #Creating base URL string for call.
    URL = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&graph=resultMap.PORTFOLIOS%5Bportfolios%5Breturns%5BperformanceChart%5D%5D%5D&identifierType=ticker&positions="
    count = 1
    for key,value in dictionary.items():
        URL += key
        URL += "~"
        URL += str(value)
        if len(dictionary.items()) != count:
            URL+="%7C"
        count += 1
    URL += "&startDate="
    #Initializing separate URL variables.
    current_time = datetime.datetime.now(datetime.timezone.utc)
    URL5Y = URL + str(int(current_time.timestamp() - (365 * 24 * 60 * 60 * 5)))
    URL1Y = URL + str(int(current_time.timestamp() - (365 * 24 * 60 * 60)))
    URL6M = URL + str(int(current_time.timestamp() - (182.5 * 24 * 60 * 60 )))
    URL3M = URL + str(int(current_time.timestamp() - (91.25 * 24 * 60 * 60)))
    URL1M = URL + str(int(current_time.timestamp() - (30.4125 * 24 * 60 * 60)))
    return URL5Y, URL1Y, URL6M, URL3M, URL1M    
