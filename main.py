import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyodide.http import open_url
import json
from js import Bokeh, JSON
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.embed import json_item
from pyscript import display, when, document, window

base_url='https://docs.google.com/spreadsheets/d/'

URL_sensorNames_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=sensorName&range=A:B'
URL_CSV_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=dataLogss&range=A:J'
URL_warn_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=warnings&range=A1'
URL_login = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=warnings&range=A20'
URL_lastEntry_aff = "/gviz/tq?tqx=out:csv;outFileName:data&sheet=last_entries&range=A:K"

page_ID = window.location.search[1:].split(',')[0]
user_ID = int(window.location.search[1:].split(',')[1])

URL_sensorNames=base_url+page_ID+URL_sensorNames_aff
URL_CSV=base_url+page_ID+URL_CSV_aff
URL_warn=base_url+page_ID+URL_warn_aff
URL_lastEntry=base_url+page_ID+URL_lastEntry_aff
names_data=pd.read_csv(open_url(URL_sensorNames))
warnings=pd.read_csv(open_url(URL_warn))
warnings2=[int(x) for x in warnings.columns[0].split(',') if x!=' ']
warnings_data=", ".join(list(names_data[names_data.ID.isin(warnings2)].Name))
last_entry=pd.read_csv(open_url(URL_lastEntry))

selected_ID=0

sensor_vars={1:["دما","رطوبت","روشنایی"], 2:["رطوبت"], 3:["دما", "ec"], 4:["CO"]}
sensor_data = pd.DataFrame

sensor_select_parent=document.querySelector('#sensor-select')

for x in names_data.Name:
    sel_item = document.createElement("option")
    sel_item.textContent = x
    sensor_select_parent.appendChild(sel_item)

@when("click", "#emergency")
def clicker(event):
    global page_ID
    document.location.href="emergency.html?"+page_ID

@when("click", "#relay")
def clickss(event):
    global page_ID
    global user_ID
    if user_ID<3:
        window.alert("هیچ دستگاه رله‌ای تعریف نشده است.")
    else:
        document.location.href="relay.html?"+page_ID

@when("click", "#update")
def click_handler(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    global selected_ID

    temp=last_entry[last_entry.ID==names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0]]
    report='Date: '+str(temp.DateTime.iloc[0])+', EC: '+str(temp.aquaEC.iloc[0])+', CO: '+str(temp.CO.iloc[0])+', T: '+str(temp.Temperature.iloc[0])+', RH: '+str(temp.RH.iloc[0])+', Lux:'+str(temp.Luminosity.iloc[0])

    element=document.getElementById("parrot1")
    element.innerHTML = warnings_data
    element2=document.getElementById("parrot2")
    element2.innerHTML = report
    selected_ID=names_data[names_data.Name==sensor_select_parent.value].ID.iloc[0].item()
    param_select=document.getElementById("parameter-select")
    param_select.innerHTML = ''
    if selected_ID<2000:
        for y in sensor_vars[1]:
            items = document.createElement("option")
            items.value = y
            items.text = y
            param_select.add(items)
    elif selected_ID>=2000 and selected_ID<3000:
        for y in sensor_vars[2]:
            items = document.createElement("option")
            items.value = y
            items.text = y
            param_select.add(items)
    elif selected_ID>=3000 and selected_ID<4000:
        for y in sensor_vars[3]:
            items = document.createElement("option")
            items.value = y
            items.text = y
            param_select.add(items)
    else:
        for y in sensor_vars[4]:
            items = document.createElement("option")
            items.value = y
            items.text = y
            param_select.add(items)

from_date=document.getElementById("start_date")
end_date=document.getElementById("end_date")

@when("click", "#fetch")
def handle_click(event):
    global sensor_data
    if selected_ID>0:
        if from_date.value=="2024-01-01" and end_date.value=="2024-01-01":
            window.alert("لطفا ابتدا تاریخ ابتدا و انتهای بازه را تعیین کنید")
        elif pd.to_datetime(from_date.value)>pd.to_datetime(end_date.value):
            window.alert("تاریخ انتهای بازه باید بزرگتر از تاریخ ابتدا باشد")
        else:
            orig_data=pd.read_csv(open_url(URL_CSV))
            orig_data=orig_data[orig_data['Time'].notna()]
            plt_data=orig_data[orig_data.ID==selected_ID].copy()
            plt_data['DateTime']=pd.to_datetime(plt_data['Date']+' '+plt_data['Time'], format='mixed')
            plt_data=plt_data.drop(['Date', 'Time'], axis=1)
            plt_data=plt_data[plt_data.DateTime>=pd.to_datetime(from_date.value)]
            plt_data=plt_data[plt_data.DateTime<=pd.to_datetime(end_date.value)]
            sensor_data=plt_data.copy()
#            param_select=documient.getElementById("parameter-select")
            if selected_ID<2000:
#                param_select.innerHTML = '';
#                for y in sensor_vars[1]:
#                    items = document.createElement("option")
#                    items.value = y
#                    items.text = y
#                    param_select.add(items)
#                    items="<option value=\""+y+"\">"+y+"</option>"
#                    param_select.innerHTML += items
#                    param_select.appendChild(items)
                p1=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Temperature [°C]", x_axis_label="DateTime")
                p1.line(plt_data['DateTime'], plt_data['Temperature [C]'], line_width=2, alpha=0.8)
                p2=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Relative Humidity[%]", x_axis_label="DateTime")
                p2.line(plt_data['DateTime'], plt_data['RH [%]'], line_width=2, alpha=0.8)
                p3=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Luminosity [Lux]", x_axis_label="DateTime")
                p3.line(plt_data['DateTime'], plt_data['Luminosity [lux]'], line_width=2, alpha=0.8)
                p = column(p1, p2, p3)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
            elif selected_ID>=2000 and selected_ID<3000:
                p=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="Temperature [°C]", x_axis_label="DateTime")
                p.line(plt_data['DateTime'], plt_data['Temperature [C]'], line_width=2, alpha=0.8)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
            elif selected_ID>=3000 and selected_ID<4000:
                p=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="EC [ugr/ml]", x_axis_label="DateTime")
                p.line(plt_data['DateTime'], plt_data['aquaEC'], line_width=2, alpha=0.8)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
            else:
                p=figure(width=800, height=250, x_axis_type="datetime", y_axis_label="CO [ppm]", x_axis_label="DateTime")
                p.line(plt_data['DateTime'], plt_data['CO'], line_width=2, alpha=0.8)
                p_json = json.dumps(json_item(p, "plotResults"))
                Bokeh.embed.embed_item(JSON.parse(p_json))
    else:
        window.alert("لطفا ابتدا سنسور موردنظر را انتخاب و به‌روزرسانی کنید")

@when("click", "#calcCumul")
def analyse_click(event):
    global sensor_data
    comp_thres=document.querySelector('#LessMore')
    value_thres=document.querySelector('#thrsValue')
    if not sensor_data.empty:
        if value_thres.value!="":
            if comp_thres.value=="کمتر از":
                sensor_data=sensor_data[sensor_data['Temperature [C]']<int(value_thres.value)]
                m, _ = sensor_data.shape
            else:
                sensor_data=sensor_data[sensor_data['Temperature [C]']>int(value_thres.value)]
                m, _ = sensor_data.shape
            dummy=0
            for i in range(1,m):
                temp=(sensor_data.DateTime.iloc[i]-sensor_data.DateTime.iloc[i-1])/ pd.Timedelta(hours=1)
                if temp<0.6:
                    dummy+=temp
            display(dummy, target="cumulative")
        else:
            window.alert("لطفا ابتدا میزان مقایسه پارامتر را وارد کنید")
    else:
        window.alert("لطفا ابتدا بازه دریافت داده را انتخاب و به‌روزرسانی کنید")

