// HTML structure for reference:
// <input type="date" id="dateInput" />
// <button id="compareButton">Compare Dates</button>
// <p id="result"></p>
base_url='https://docs.google.com/spreadsheets/d/';

const queryString = window.location.search.slice(1);
const page_ID = queryString.split(',')[0]; // Replace with your spreadsheet ID
const user_ID = queryString.split(',')[1]; // Replace with your user ID
const range = 'dataLogss!A1:J100';              // Adjust range as needed
const apiKey = 'AIzaSyDs8PBqXI4X-kVOYsVOlqydjaleyVUIFbc';               // Replace with your API key

const URL_sensorNames_aff = '/gviz/tq?tqx=out:json&sheet=sensorName&range=A:B';
const URL_CSV_aff = '/gviz/tq?tqx=out:json&sheet=dataLogss&range=A:J';
const URL_warn_aff = '/gviz/tq?tqx=out:json&sheet=warnings&range=A1';
const URL_lastEntry_aff = "/gviz/tq?tqx=out:json&sheet=last_entries&range=A:K";

const parameter = queryString.split(',')[1]

const URL_sensorNames=`${base_url}${page_ID}${URL_sensorNames_aff}`;
const URL_CSV=`${base_url}${page_ID}${URL_CSV_aff}`;
const URL_warn=`${base_url}${page_ID}${URL_warn_aff}`;
const URL_lastEntry=`${base_url}${page_ID}${URL_lastEntry_aff}`;

var IDArray;
var selectedID;
let plotArray=[];

async function fetchSensorNames(urlName) {
    const url = `${urlName}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }
        // The response is wrapped in a Google Visualization response; strip it
        const text = await response.text();
        const jsonMatch = text.match(/google\.visualization\.Query\.setResponse\(([\s\S]*)\);/);
        if (!jsonMatch || !jsonMatch[1]) {
            throw new Error('Failed to extract JSON payload from response');
        }

        let data;
        try {
            data = JSON.parse(jsonMatch[1]);
        } catch (parseError) {
            console.error('JSON Parsing Error:', parseError);
            console.error('Raw Response:', text);
            console.error('Extracted JSON String:', jsonMatch[1]);
            throw new Error('Invalid JSON format in response');
        }
        
        // Extract rows from the table
        const rows = data.table.rows;
        // Process data: Skip header row implicitly, convert to [timestamp, value]
        const chartData = rows.map(row => {
            const nameStr = row.c[0]?.v; // First column: Date
            const ID = row.c[1]?.v;   // Second column: Value
            return [nameStr, ID];
        }).filter(point => point !== null);
        return chartData;
    }  catch (error) {
        console.error('Error fetching Google Sheets data:', error);
        document.getElementById('container').innerText = 'Failed to load data. Check console for details.';
    }
}

async function fetchWarnings(urlName) {
    const url = `${urlName}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }
        // The response is wrapped in a Google Visualization response; strip it
        const text = await response.text();
        const jsonMatch = text.match(/google\.visualization\.Query\.setResponse\(([\s\S]*)\);/);
        if (!jsonMatch || !jsonMatch[1]) {
            throw new Error('Failed to extract JSON payload from response');
        }

        let data;
        try {
            data = JSON.parse(jsonMatch[1]);
        } catch (parseError) {
            console.error('JSON Parsing Error:', parseError);
            console.error('Raw Response:', text);
            console.error('Extracted JSON String:', jsonMatch[1]);
            throw new Error('Invalid JSON format in response');
        }
        
        // Extract rows from the table
        const rows = data.table.rows;
        // Process data: Skip header row implicitly, convert to [timestamp, value]
        const chartData = rows.map(row => {
            const warns = row.c[0]?.v; // First column: Date
            return warns;
        }).filter(point => point !== null);
        return chartData;
    }  catch (error) {
        console.error('Error fetching Google Sheets data:', error);
        document.getElementById('container').innerText = 'Failed to load data. Check console for details.';
    }
}

// Function to add options to a select field
function addOptionsToSelect(selectId, options) {
    const selectElement = document.getElementById(selectId);
    if (!selectElement) {
        console.error(`Select element with id "${selectId}" not found.`);
        return;
    }

    options.forEach(option => {
        const newOption = document.createElement('option');
        newOption.value = option.value;
        newOption.textContent = option.text;
        selectElement.appendChild(newOption);
    });
}

fetchSensorNames(URL_sensorNames).then(data =>  {
    console.log(data);
    document.getElementById('parrot2').innerHTML=data[0][0];
    IDArray=data;
    for (var i = 0; i < data.length; i++) {
        var options = [{ value: data[i][0], text: data[i][0] }];
        addOptionsToSelect('sensor-select', options);
    }
    });

fetchWarnings(URL_warn).then(data =>  {
    console.log(data);
    document.getElementById('parrot1').innerHTML=data;
    });

// Fetch and process data from Google Sheets
async function fetchPlotData(urlName) {
    const url = `${urlName}`;
    try {
        // Fetch the data
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const text = await response.text();
        const jsonMatch = text.match(/google\.visualization\.Query\.setResponse\(([\s\S]*)\);/);
        if (!jsonMatch || !jsonMatch[1]) {
            throw new Error('Failed to extract JSON payload from response');
        }

        // Parse the JSON data
        let data;
        try {
            data = JSON.parse(jsonMatch[1]);
        } catch (parseError) {
            console.error('JSON Parsing Error:', parseError);
            throw new Error('Invalid JSON format in response');
        }

        if (!data.table || !data.table.cols || !data.table.rows) {
            throw new Error('Invalid data structure in response');
        }

        // Extract series names from column headers (columns 3 to 10)
        const cols = data.table.cols;
        const seriesNames = [];
        for (let i = 2; i < 10; i++) {
            seriesNames.push(cols[i]?.label || `Series ${i - 1}`);
        }

        // Initialize arrays for the eight series' data
        const seriesData = Array.from({ length: 8 }, () => []);
        const rows = data.table.rows;

        // Process each row
        rows.forEach(row => {
            const dateStr = row.c[0]?.f; // First column: date
            // let date;
            // if (typeof dateStr === 'string' && dateStr.startsWith('Date(')) {
            //     // Parse Google Sheets Date format, e.g., "Date(2023,0,1)"
            //     const match = dateStr.match(/Date\((\d+),(\d+),(\d+)\)/);
            //     if (match) {
            //         date = new Date(match[1], match[2], match[3]);
            //     }
            // } else {
            //     console.warn("we're here");
            //     date = new Date(dateStr);
            // }
            const timeStr = row.c[1]?.v; // Second column: time
            if (dateStr && timeStr) {
                // Combine date and time into a datetime string
                const datetimeStr = `${dateStr} ${timeStr}:00`;
                const timestamp = new Date(datetimeStr).getTime();
                
                // Check if the timestamp is valid
                if (!isNaN(timestamp)) {
                    // Extract data from columns 3 to 10 (indices 2 to 9)
                    for (let i = 0; i < 8; i++) {
                        const yValue = parseInt(row.c[i + 2]?.v);
                        // Convert to number if possible, otherwise use null
                        const y = typeof yValue === 'number' ? yValue : null;
                        seriesData[i].push([timestamp, y]);
                    }
                } else {
                    console.warn(`Invalid datetime: ${datetimeStr}`);
                }
            } else {
                console.warn('Missing date or time in row');
            }
        });

        // Sort each series by timestamp to ensure proper rendering
        seriesData.forEach(data => data.sort((a, b) => a[0] - b[0]));

        // Create series objects for Highcharts
        const series = seriesData.map((data, i) => ({
            name: seriesNames[i],
            data: data
        }));

        return series;
    } catch (error) {
        console.error('Error fetching Google Sheets data:', error);
        document.getElementById('container').innerText = 'Failed to load data. Check console for details.';
    }
}

// Render the chart using Highcharts
function renderChart(series) {
    Highcharts.chart('plotResults', {
        chart: {
            type: 'line',
            zoomType: 'x' // Enable zooming on the x-axis
        },
        title: {
            text: 'Google Sheets Data Visualization'
        },
        xAxis: {
            type: 'datetime',
            title: { text: 'Date and Time' },
            minRange: 1
        },
        yAxis: {
            title: { text: 'Values' }
        },
        tooltip: {
            shared: true, // Show all series values in the tooltip
            valueDecimals: 2
        },
        series: series,
        responsive: {
            rules: [{
                condition: { maxWidth: 500 },
                chartOptions: { legend: { enabled: false } }
            }]
        }
    });
}

document.getElementById('emergency').addEventListener('click', function () {
    document.location.href = `/emergency.html?${page_ID},${user_ID}`;
});

document.getElementById('relay').addEventListener('click', function () {
    if(user_ID<3) {
        window.alert("هیچ دستگاه رله‌ای تعریف نشده است.");
    } else {
        document.location.href=`/relay.html?${page_ID},${user_ID}`;
    }
});

function getAllIndexes(arr,val) {
    var indexes = [], i;
    for(i=0; i<arr.length; i++)
        if(arr[i]===val)
            indexes.push(i);
    return indexes;
}

document.getElementById('update').addEventListener('click', function () {
    const selectedName = document.getElementById('sensor-select').value;
    for (var i = 0; i < IDArray.length; i++) {
        if(IDArray[i][0]==selectedName) {
            selectedID=IDArray[i][1];
        }
    }
    console.log(selectedID);
    if(plotArray.length==0) {
        fetchPlotData(URL_CSV).then(data =>  {
            plotArray=data;
            console.log(plotArray);
            var categories = plotArray[0].data.map(x => x[1]);
            var indexes = getAllIndexes(categories, selectedID);
            // Filter the series (excluding the "ID" series)
            var filteredSeries = plotArray.slice(1).map(function(series) {
                var filteredData = indexes.map(function(index) {
                    return series.data[index];
                });
                return {
                    name: series.name,
                    data: filteredData
                };
            });
            console.log(filteredSeries);
            // Render the chart
            renderChart(filteredSeries);
        });
    } else {
        console.log(plotArray);
        var categories = plotArray[0].data.map(x => x[1]);
        var indexes = getAllIndexes(categories, selectedID);
        // Filter the series (excluding the "ID" series)
        var filteredSeries = plotArray.slice(1).map(function(series) {
            var filteredData = indexes.map(function(index) {
                return series.data[index];
            });
            return {
                name: series.name,
                data: filteredData
            };
        });
        console.log(filteredSeries);
        // Render the chart
        renderChart(filteredSeries);
    }
    //TODO1: get the main data only if it's empty (the first time)
    //TODO2: plot the sensor
});
// document.getElementById('fetch_date').addEventListener('click', function () {
//     const startDate = new Date(document.getElementById('start_date').value);
//     const comparisonDate = new Date('2023-12-31'); // Example comparison date

//     if (isNaN(inputDate.getTime())) {
//         document.getElementById('result').textContent = 'Please enter a valid date.';
//         return;
//     }

//     if (inputDate < comparisonDate) {
//         document.getElementById('result').textContent = 'The input date is earlier than the comparison date.';
//     } else if (inputDate > comparisonDate) {
//         document.getElementById('result').textContent = 'The input date is later than the comparison date.';
//     } else {
//         document.getElementById('result').textContent = 'The input date is the same as the comparison date.';
//     }
// });