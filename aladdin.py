import requests
import json

"""
For the examples we are using 'requests' which is a popular minimalistic python library for making HTTP requests.
Please use 'pip install requests' to add it to your python libraries.
"""


"""
epoch_time: time index 
time_overall_percentage_dict: [d[epoch time, percentage compared to 100%]]
overall_percentage: percentage changes compared to when market first opens
daily_percentage: (cur_percentage - prev_percentage) / prev_percentage
"""

def getGraphVals(json_obj):
	time_overall_percentage_dict = json_obj['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['performanceChart']
	epoch_time = [row[0] for row in time_overall_percentage_dict]
	overall_percentage = [row[1] for row in time_overall_percentage_dict]

	daily_percentage = [(1)]
	for i in range(1, len(overall_percentage)):
		daily_percentage.append(overall_percentage[i] - overall_percentage[i-1] / overall_percentage[i-1])

	return epoch_time, time_overall_percentage_dict, overall_percentage, daily_percentage

def getResponse(url = "https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&graph=resultMap.PORTFOLIOS%5Bportfolios%5Breturns%5BperformanceChart%5D%5D%5D&identifierType=ticker&positions=VZ~25%7CWMT~25%7CFB~25%7CAAPL~25&startDate=1522400400"):
	portfolioAnalysisRequest = requests.get(url)
	t = portfolioAnalysisRequest.text # get in text string format, same as json.dumps()
	json_obj = json.loads(t) # string to json, returns a dict of [epoch time, percentage compared to 100%]
	
	return getGraphVals(json_obj)

