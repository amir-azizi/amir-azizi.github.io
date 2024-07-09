import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyodide.http import open_url
#import hvplot.pandas
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import panel as pn
from pyscript import display
#from js import documenti
from pyscript import when, document, window

URL_sensorNames = 'https://docs.google.com/spreadsheets/d/1p1_QuuhkRShcVdWlMDurQWs-VLerXEUU9bXS3dLEofQ/gviz/tq?tqx=out:csv;outFileName:data&sheet=sensorNames&range=A:B'
URL_CSV = 'https://docs.google.com/spreadsheets/d/1p1_QuuhkRShcVdWlMDurQWs-VLerXEUU9bXS3dLEofQ/gviz/tq?tqx=out:csv;outFileName:data&sheet=dataLogs&range=A:J'
URL_warn = 'https://docs.google.com/spreadsheets/d/1p1_QuuhkRShcVdWlMDurQWs-VLerXEUU9bXS3dLEofQ/gviz/tq?tqx=out:csv;outFileName:data&sheet=warnings&range=A2'
URL_lastEntry = "https://docs.google.com/spreadsheets/d/1p1_QuuhkRShcVdWlMDurQWs-VLerXEUU9bXS3dLEofQ/gviz/tq?tqx=out:csv;outFileName:data&sheet=last_entry&range=A:K"

names_data=pd.read_csv(open_url(URL_sensorNames))
warnings_data=open_url(URL_warn)
last_entry=pd.read_csv(open_url(URL_lastEntry))

sensor_select_parent=document.querySelector('#sensor-select')
for x in names_data.Name:
    sel_item = document.createElement("option")
    sel_item.textContent = x
    sensor_select_parent.appendChild(sel_item)

@when("click", "#update")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    temp=last_entry[last_entry.ID==names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0]]
    report='Date: '+str(temp.DateTime.iloc[0])+', EC: '+str(temp.aquaEC.iloc[0])+', CO: '+str(temp.CO.iloc[0])+', T: '+str(temp.Temperature.iloc[0])+', RH: '+str(temp.RH.iloc[0])+', Lux:'+str(temp.Luminosity.iloc[0])

    element=document.getElementById("parrot1")
    element.innerHTML = warnings_data.getvalue()
    element2=document.getElementById("parrot2")
    element2.innerHTML = report
#select = pn.widgets.Select(name='انتخاب حسگر', options=[x for x in names_data.Name]).servable(target='sensor-select')

from_date=document.getElementById("start_date")
end_date=document.getElementById("end_date")

@when("click", "#fetch")
def handle_click(event):
#    display(from_date.value, target="returnDates")
#    element.write(from_date.value)
    if from_date.value=="2024-01-01" and end_date.value=="2024-01-01":
        window.alert("لطفا ابتدا تاریخ ابتدا و انتهای بازه را تعیین کنید")
    else:
        orig_data=pd.read_csv(open_url(URL_CSV))
        orig_data=orig_data[orig_data['Time'].notna()]
        selected_ID=names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0].item()
        plt_data=orig_data[orig_data.ID==selected_ID].copy()
        plt_data['DateTime']=pd.to_datetime(plt_data['Date']+' '+plt_data['Time'], format='mixed')
        plt_data=plt_data.drop(['Date', 'Time'], axis=1)
        plt_data=plt_data[plt_data.DateTime>=pd.to_datetime(from_date.value)]
        plt_data=plt_data[plt_data.DateTime<=pd.to_datetime(end_date.value)]
        display(str(orig_data.shape)+" "+from_date.value+" "+str(plt_data.shape), target="plotStatus")
        if selected_ID<2000:
            fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
            plt_data.plot(x='DateTime', y='Temperature [C]', ax=axes[0])
            plt_data.plot(x='DateTime', y='RH [%]', ax=axes[1])
            plt_data.plot(x='DateTime', y='Luminosity [lux]', ax=axes[2])
            display(fig, target="plotResults")

