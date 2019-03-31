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
	value_list = [d['value'] for d in exposures]
	y_list = [d['y'] for d in exposures] 
	
	print(value_list, y_list)
	return value_list, y_list

def getResponse(option, url): # option: {1,2} 1:getPortfolioAnalysis called 2: getExposure called
	portfolioAnalysisRequest = requests.get(url)
	t = portfolioAnalysisRequest.text # get in text string format, same as json.dumps()
	json_obj = json.loads(t) # string to json, returns a dict of [epoch time, percentage compared to 100%]

	if option == 1:
		res = getPortfolioAnalysis(json_obj)
	else:
		res = getExposure(json_obj)	

	return res

# portfolio_analysis = getResponse(1, "https://www.blackrock.com/tools/hackathon/portfolio-analysis?calculateExposures=true&calculatePerformance=true&graph=resultMap.PORTFOLIOS%5Bportfolios%5Breturns%5BperformanceChart%5D%5D%5D&identifierType=ticker&positions=VZ~25%7CWMT~25%7CFB~25%7CVWO~25&startDate=1522400400")
# exposures = getResponse(2, "https://www.blackrock.com/tools/hackathon/portfolio-analysis?betaPortfolios=SNP500&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&positions=AAPL~25%7CVWO~25%7CAGG~25%7CMALOX~25%7C&riskFreeRatePortfolio=LTBILL1-3M&scenarios=HIST_20081102_20080911%2CHIST_20110919_20110720%2CHIST_20130623_20130520%2CHIST_20140817_20140101%2CUS10Y_1SD%3A%3AAPB%2CINF2Y_1SD%3A%3AAPB%2CUSIG_1SD%3A%3AAPB%2CSPX_1SD%3A%3AAPB%2CDXY_1SD%3A%3AAPB")



