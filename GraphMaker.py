# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 20:35:48 2019

@author: Ohad Michel
"""
import matplotlib.pyplot as plt
import numpy as np
from aladdin import getResponse
from URLMaker import URLMaker
import datetime
import io, base64

def save_to_tmp_file():
    '''
    Saves an in memory image
    '''
    sio = io.BytesIO()
    plt.savefig(sio, format='png')
    sio.seek(0)
    buffer = sio.getvalue()
    b64 = base64.b64encode(buffer)
    
    return b64

current_time = datetime.datetime.now(datetime.timezone.utc)
defaultstartdate = int(current_time.timestamp() - (360 * 24 * 60 * 60 * 5))
def GraphMaker(portfolio, startdate = defaultstartdate):
    """
    Plots and saves graphs for: the entire data from start date and on, last 30 days,
    last 90 days, last 150 days and last year (360 days)
    
    Inputs:
        portfolio - a dictionary {ticker:percent,...}, percents must sum up to 100!
        startdate - start date in epoch time
    outputs:
        image_dict - a dictionary of in memory graph images
    """
    image_dict = {} # allocate space for a dictionary of images
    url = URLMaker(portfolio) # make a URL for the requested portfolio dict
    dict_, overall_percentage, daily_percentage = getResponse(url) # get API response
    t = np.arange(len(daily_percentage)) # a time series in units of days
    
    # Convert to np arrays
    overall_percentage = np.array(overall_percentage)
    daily_percentage = np.array(daily_percentage)
    
    # find positive and negative ranges for daily_percentage
    negbar_ind = daily_percentage<0 # indices of negative value bars
    posbar_ind = daily_percentage>=0 # indices of negative value bars
    
    ''' Plotting '''
    plt.figure(figsize = (10,5))
    plt.rcParams.update({'font.size': 16})
    
    # Plot overall stock return
    plt.plot(t, overall_percentage, linewidth=3, alpha=0.75)
    
    # Plot positive daily change bars
    plt.bar(t[posbar_ind], daily_percentage[posbar_ind], width=0.8, alpha=0.95, color='g')
    
    # Plot negative daily change bars
    plt.bar(t[negbar_ind], daily_percentage[negbar_ind], width=0.8, alpha=0.95, color='r')
    
    # Change background color
    ax = plt.gca()
    ax.set_facecolor((36/255,39/255,38/255))
    
    # Axis labels
    plt.xlabel('time (days)')
    plt.ylabel('percentage')
    plt.grid()
    image = save_to_tmp_file()
    image_dict['full'] = image
    
    ''' Plotting specific ranges '''
    # A list of time spans for graphs
    timespans_strings = ['30', '90', '150', '360']
    timespan_list = [t>t[-1]-30, t>t[-1]-90, t>t[-1]-150, t>t[-1]-360]
    
    for i, timespan in enumerate(timespan_list):
    
        plt.figure(figsize = (10,5))
        plt.rcParams.update({'font.size': 16})
    
        # Plot overall stock return
        plt.plot(t[timespan], overall_percentage[timespan], linewidth=3, alpha=0.75)
    
        # Plot positive daily change bars
        plt.bar(t[timespan & posbar_ind], daily_percentage[timespan & posbar_ind], width=0.8, alpha=0.95, color='g')
    
        # Plot negative daily change bars
        plt.bar(t[timespan & negbar_ind], daily_percentage[timespan & negbar_ind], width=0.8, alpha=0.95, color='r')
    
        # Change background color
        ax = plt.gca()
        ax.set_facecolor((36/255,39/255,38/255))
    
        # Axis labels
        plt.xlabel('time (days)')
        plt.ylabel('percentage')
        plt.grid()
        image = save_to_tmp_file()
        image_dict[timespans_strings[i]] = image

    return image_dict
        
#GraphMaker({"AAPL":35, "NFLX":25, "FB":10, "MSFT":30})