from aladdin import getResponse, getExposure, getPortfolioAnalysis
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

"""
graphs exposure percentages in a pie chart
"""
(name_list, y_list) = getResponse("https://www.blackrock.com/tools/hackathon/portfolio-analysis?betaPortfolios=SNP500&calculateExposures=true&calculatePerformance=true&calculateRisk=true&calculateStressTests=true&positions=AAPL~25%7CVWO~25%7CAGG~25%7CMALOX~25%7C&riskFreeRatePortfolio=LTBILL1-3M&scenarios=HIST_20081102_20080911%2CHIST_20110919_20110720%2CHIST_20130623_20130520%2CHIST_20140817_20140101%2CUS10Y_1SD%3A%3AAPB%2CINF2Y_1SD%3A%3AAPB%2CUSIG_1SD%3A%3AAPB%2CSPX_1SD%3A%3AAPB%2CDXY_1SD%3A%3AAPB", 2)

# Data to plot
n = len(name_list)
cs=cm.Set1(np.arange(n)/n)

labels = name_list
sizes = y_list
colors = cs
 
# Plot
plt.pie(sizes, labels=labels, colors=colors,
			   autopct='%1.1f%%', shadow=True, startangle=140)
plt.legend(labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.axis('equal')
plt.show()
