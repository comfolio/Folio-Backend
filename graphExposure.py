from aladdin import getResponse
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from URLMaker import URLMakerExposure
from GraphMaker import save_to_tmp_file

"""
graphs exposure percentages in a pie chart
"""
def PieMaker(portfolio):
    
    url = URLMakerExposure(portfolio)
    [name_list, y_list] = getResponse(url, 2)
    
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
    image = save_to_tmp_file()
    
    return image

PieMaker({"AAPL":25, "VWO":25, "AGG":25, "MALOX":25})