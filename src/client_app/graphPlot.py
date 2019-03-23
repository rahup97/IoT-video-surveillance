# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 22:48:53 2017

@author: rramess
"""

import datetime, pymysql
from numpy import pi, arange, sin, linspace
from collections import defaultdict
from bokeh.plotting import output_file, figure, show
from bokeh.models import LinearAxis, Range1d
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd



#get data from database
#now = datetime.datetime.now()
#print ("Current date and time : ")
#print (now.year)

def plot1():

    db = pymysql.connect(host='surveillance.ciaezgtf2rvc.us-west-2.rds.amazonaws.com',
                                 user='surveillancess',
                                 password='rohith201',
                                 db='HOME_SURVEILLANCE',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print("Successfully connected to database.");

    cur = db.cursor(pymysql.cursors.DictCursor)

    #STORE ALL MOTION IDS
    exit_times=[]
    entry_times=[]
    motion_ids=[]

    sql = "SELECT * FROM Motion_Detection;"
    cur.execute(sql)
    for row in cur:
        exit_times.append((row['exit_time']))
        motion_ids.append((row['motionid']))
        #exit_times.append((row['exit_time']))
        entry_times.append((row['entry_time']))


    #print(exittimes)

    print (exit_times)
    print (entry_times)

    data = defaultdict(list)

    for element in exit_times:
        data['exit'].append(element)

    for element in entry_times:
        data['entry'].append(element)

    for element in motion_ids:
        data['motion_id'].append(element)

    df = pd.DataFrame(data)
    df['entry'] = pd.to_datetime(df['entry'])
    df['exit'] = pd.to_datetime(df['exit'])

    p = figure(plot_width=800, plot_height=400, title = "Entry Time vs. Exit Time: Line Graphs", x_axis_type="datetime", x_axis_label="Time", y_axis_label="Motion ID")

    p.line(df['entry'], df['motion_id'], color='crimson', alpha=1.5, legend='Entry time')
    p.circle(df['entry'], df['motion_id'], size=20, color="crimson", alpha=0.5)

    p.line(df['exit'], df['motion_id'], color='indigo', alpha=1.5, legend='Exit time')
    p.circle(df['exit'], df['motion_id'], size=20, color="indigo", alpha=0.5)
    
    

    p.legend.location = "top_left"
    print(df)

    output_file("datetime.html")
    show(p)
    
    
def plot2():
    
    db = pymysql.connect(host='surveillance.ciaezgtf2rvc.us-west-2.rds.amazonaws.com',
                                 user='surveillancess',
                                 password='rohith201',
                                 db='HOME_SURVEILLANCE',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    print("Successfully connected to database.");

    cur = db.cursor(pymysql.cursors.DictCursor)
    
    #STORE ALL MOTION IDS
    exit_times=[]
    entry_times=[]
    motion_ids=[]

    sql = "SELECT * FROM Motion_Detection;"
    cur.execute(sql)
    for row in cur:
        exit_times.append((row['exit_time']))
        motion_ids.append((row['motionid']))
        #exit_times.append((row['exit_time']))
        entry_times.append((row['entry_time']))


    #print(exittimes)

    print (exit_times)
    print (entry_times)

    data = defaultdict(list)

    for element in exit_times:
        data['exit'].append(element)

    for element in entry_times:
        data['entry'].append(element)

    for element in motion_ids:
        data['motion_id'].append(element)

    df = pd.DataFrame(data)
    df['entry'] = pd.to_datetime(df['entry'])
    df['exit'] = pd.to_datetime(df['exit'])
    
    plot = figure(height = 150, width = 400, title = "Graph for Time Periods of Detection", x_axis_type = "datetime", responsive = True)

    plot.title.text = "Motion Detection plot"
    plot.xaxis.axis_label = "Time of Detection"
    plot.yaxis.minor_tick_line_color = None
    plot.ygrid[0].ticker.desired_num_ticks = 1

    plot.quad(top = 1, bottom = 0, left = "entry", right = "exit", color = "green", alpha = 0.8, source = df)

    output_file("Plot2.html")
    show(plot)
