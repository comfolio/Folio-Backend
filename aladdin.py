import requests
import json
from pprint import pprint

from URLMaker import URLMaker

"""
For the examples we are using 'requests' which is a popular minimalistic python library for making HTTP requests.
Please use 'pip install requests' to add it to your python libraries.
"""


"""
time_overall_percentage_dict: [d[epoch time, percentage compared to 100%]]
overall_percentage: percentage changes compared to when market first opens
daily_percentage: (cur_percentage - prev_percentage) / prev_percentage
"""

def getPortfolioAnalysis(json_obj):
	# pprint(json_obj)
	time_overall_percentage_dict = json_obj['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['returns']['performanceChart']

	overall_percentage = [row[1] for row in time_overall_percentage_dict]
	daily_percentage = [(0)]
	for i in range(1, len(overall_percentage)):
		daily_percentage.append((overall_percentage[i] - overall_percentage[i-1]) / overall_percentage[i-1] * 100)

	overall_percentage = [v-1 for v in overall_percentage]

	return time_overall_percentage_dict, overall_percentage, daily_percentage

def getExposure(json_obj):
	# pprint(json_obj)
	exposures = json_obj['resultMap']['PORTFOLIOS'][0]['portfolios'][0]['exposures']['assetClass']
	name_list = [d['name'] for d in exposures]
	y_list = [d['y'] for d in exposures] 
	
	print(name_list, y_list)
	return name_list, y_list

def getResponse(url, option): # option: {1,2} 1:getPortfolioAnalysis called 2: getExposure called
	portfolioAnalysisRequest = requests.get(url)
	t = portfolioAnalysisRequest.text # get in text string format, same as json.dumps()
	json_obj = json.loads(t) # string to json, returns a dict of [epoch time, percentage compared to 100%]

	if option == 1:
		res = getPortfolioAnalysis(json_obj)
	else:
		res = getExposure(json_obj)	

	return res


