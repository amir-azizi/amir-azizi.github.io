import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
from pyodide.http import open_url, pyfetch
import asyncio
import json
from js import Bokeh, JSON, XMLHttpRequest, console
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.embed import json_item
from pyscript import display, when, document, window, fetch

import requests

base_url='https://docs.google.com/spreadsheets/d/'

URL_sensorNames_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=sensorName&range=A:B'
URL_CSV_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=dataLogss&range=A:J'
URL_lastEntry_aff = "/gviz/tq?tqx=out:csv;outFileName:data&sheet=last_entries&range=A:K"
URL_emergencies_aff = '/gviz/tq?tqx=out:csv;outFileName:data&sheet=emergencies&range=A2:G'

POST_URL='https://script.google.com/macros/s/AKfycbwGbbEgWMTogmDnScLhFz5aUYv3ejmSjtyhDgwp26bEkMmiLVOJQs1rl9O5OMGRIXqW/exec'
page_ID = window.location.search[1:]

URL_sensorNames=base_url+page_ID+URL_sensorNames_aff
URL_CSV=base_url+page_ID+URL_CSV_aff
URL_lastEntry=base_url+page_ID+URL_lastEntry_aff
URL_emergencies=base_url+page_ID+URL_emergencies_aff
names_data=pd.read_csv(open_url(URL_sensorNames))
last_entry=pd.read_csv(open_url(URL_lastEntry))
emergencies=pd.read_csv(open_url(URL_emergencies), header=None).values.tolist()


def make_post_request(datas):
    # Create the XMLHttpRequest object
    xhr = XMLHttpRequest.new()

    # Configure it: POST request, asynchronous
    xhr.open("POST", POST_URL, True)
    xhr.setRequestHeader("Content-Type", "application/json")
    
    # Define the response handler
    def on_ready_state_change(*args):
        if xhr.readyState == 4:  # Request is complete
            if xhr.status == 200:  # Success
                console.log("Response:", xhr.responseText)
            else:  # Error
                console.error("Error:", xhr.status, xhr.statusText)
    
    # Attach the handler
    xhr.onreadystatechange = on_ready_state_change
    
    # Send the request
    xhr.send(json.dumps(datas))


data={"command": "4", "sheet_name": "emergencies", "values": "2025,R,L,0,1234,567,0"}
letsSee= ""
make_post_request(data)
element=document.getElementById("dbScreen")
element.innerHTML = letsSee

selected_ID=0

sensor_vars={1:["دما","رطوبت","روشنایی"], 2:["رطوبت"], 3:["دما", "ec"], 4:["CO"]}
sensor_data = pd.DataFrame

sensor_select_parent1=document.querySelector('#sensor-select1')
for x in names_data.Name:
    sel_item = document.createElement("option")
    sel_item.textContent = x
    sensor_select_parent1.appendChild(sel_item)
sensor_select_parent2=document.querySelector('#sensor-select2')
for x in names_data.Name:
    sel_item = document.createElement("option")
    sel_item.textContent = x
    sensor_select_parent2.appendChild(sel_item)
sensor_select_parent3=document.querySelector('#sensor-select3')
for x in names_data.Name:
    sel_item = document.createElement("option")
    sel_item.textContent = x
    sensor_select_parent3.appendChild(sel_item)

@when("click", "#sensorSel1")
def click_handler1(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    selected_ID=names_data[names_data.Name==sensor_select_parent1.value].ID.iloc[0].item()
    param_select=document.getElementById("parameter-select1")
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

@when("click", "#sensorSel2")
def click_handler2(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    selected_ID=names_data[names_data.Name==sensor_select_parent2.value].ID.iloc[0].item()
    param_select=document.getElementById("parameter-select2")
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

@when("click", "#sensorSel3")
def click_handler3(event):
    """
    Event handlers get an event object representing the activity that raised
    them.
    """
    selected_ID=names_data[names_data.Name==sensor_select_parent3.value].ID.iloc[0].item()
    param_select=document.getElementById("parameter-select3")
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

def post_data(datas):
    #response = await pyfetch(
    response = fetch(
        POST_URL,
        method="POST",
        headers={"Content-Type": "application/json"},
        #body=datas
        body=json.dumps(datas)
    )

    print("I'm here!")
    if response.ok:
        result = response.text()
        window.alert("{}".format(result))
    else:
        window.alert("ﺎﺨﻃﺍﺭ ﺚﺒﺗ ﻦﺷﺩ. ﻞﻄﻓﺍ ﺩﻮﺑﺍﺮﻫ ﺕﻼﺷ ﮏﻨﯾﺩ.")


def handle_response(xhr):
    if xhr.readyState == 4 and xhr.status == 200:
        response = json.parse(xhr.responseText)
        window.alert("{}".format(response))
    else:
        window.alert("ﺎﺨﻃﺍﺭ ﺚﺒﺗ ﻦﺷﺩ. ﻞﻄﻓﺍ ﺩﻮﺑﺍﺮﻫ ﺕﻼﺷ ﮏﻨﯾﺩ.")

@when("click", "#calcCumul1")
def analyse_click1(event):
    selected_ID=names_data[names_data.Name==sensor_select_parent1.value].ID.iloc[0].item()
    param_select=document.querySelector("#parameter-select1")
    parameters=""
    
    phone="912841"

    comp_thres=document.querySelector('#LessMore1')
    value_thres=document.querySelector('#thrsValue1')
    less_more=""
    if value_thres.value!="":
        if comp_thres.value=="کمتر از":
            less_more="L"
        else:
            less_more="G"
    else:
        window.alert("لطفا ابتدا میزان مقایسه پارامتر را وارد کنید")
    if selected_ID<2000:
        if param_select.value=="دما":
            parameters="T"
        elif param_select.value=="رطوبت":
            parameters="R"
        else:
            parameters="L"
    elif selected_ID>=2000 and selected_ID<3000:
        if param_select.value=="رطوبت":
            parameters="H"
    elif selected_ID>=3000 and selected_ID<4000:
        if param_select.value=="دما":
            parameters="T"
        else:
            parameters="E"
    else:
        if param_select.value=="CO":
            parameters="C"

    data = {"command": "2", "sheet_name": "emergencies", "values": "{},{},{},{},{}".format(selected_ID,parameters,less_more,value_thres.value,phone)}

    x = requests.post(POST_URL, json=data)
    window.alert(x.text)
#    make_post_request(data)
#    post_data(data)
    #asyncio.run(post_data(data))

@when("click", "#calcCumul2")
def analyse_click2(event):
    selected_ID=names_data[names_data.Name==sensor_select_parent2.value].ID.iloc[0].item()
    param_select=document.querySelector("#parameter-select2")
    parameters=""
    
    phone="912841"

    comp_thres=document.querySelector('#LessMore2')
    value_thres=document.querySelector('#thrsValue2')
    less_more=""
    if value_thres.value!="":
        if comp_thres.value=="کمتر از":
            less_more="L"
        else:
            less_more="G"
    else:
        window.alert("لطفا ابتدا میزان مقایسه پارامتر را وارد کنید")
    if selected_ID<2000:
        if param_select.value=="دما":
            parameters="T"
        elif param_select.value=="رطوبت":
            parameters="R"
        else:
            parameters="L"
    elif selected_ID>=2000 and selected_ID<3000:
        if param_select.value=="رطوبت":
            parameters="H"
    elif selected_ID>=3000 and selected_ID<4000:
        if param_select.value=="دما":
            parameters="T"
        else:
            parameters="E"
    else:
        if param_select.value=="CO":
            parameters="C"

    data = {"command": "3", "sheet_name": "emergencies", "values": "{},{},{},{},{}".format(selected_ID,parameters,less_more,value_thres.value,phone)}

    x = requests.post(POST_URL, json=data)
    window.alert(x.text)
    #make_post_request(data)
#    post_data(data)
    #asyncio.run(post_data(data))

@when("click", "#calcCumul3")
def analyse_click3(event):
    selected_ID=names_data[names_data.Name==sensor_select_parent3.value].ID.iloc[0].item()
    param_select=document.querySelector("#parameter-select3")
    parameters=""
    
    phone="912841"

    comp_thres=document.querySelector('#LessMore3')
    value_thres=document.querySelector('#thrsValue3')
    less_more=""
    if value_thres.value!="":
        if comp_thres.value=="کمتر از":
            less_more="L"
        else:
            less_more="G"
    else:
        window.alert("لطفا ابتدا میزان مقایسه پارامتر را وارد کنید")
    if selected_ID<2000:
        if param_select.value=="دما":
            parameters="T"
        elif param_select.value=="رطوبت":
            parameters="R"
        else:
            parameters="L"
    elif selected_ID>=2000 and selected_ID<3000:
        if param_select.value=="رطوبت":
            parameters="H"
    elif selected_ID>=3000 and selected_ID<4000:
        if param_select.value=="دما":
            parameters="T"
        else:
            parameters="E"
    else:
        if param_select.value=="CO":
            parameters="C"

    data = {"command": "4", "sheet_name": "emergencies", "values": "{},{},{},{},{}".format(selected_ID,parameters,less_more,value_thres.value,phone)}

    x = requests.post(POST_URL, json=data)
    window.alert(x.text)
    #make_post_request(data)
    #post_data(data)
    #asyncio.run(post_data(data))

