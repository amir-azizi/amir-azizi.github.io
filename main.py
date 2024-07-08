import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyodide.http import open_url
#import hvplot.pandas
#import numpy as np
import pandas as pd
#import panel as pn
from pyscript import display
#from js import documenti
from pyscript import when, document

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
